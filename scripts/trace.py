#!/usr/bin/env python3
"""spec-flow traceability checker.

Builds a REQ <-> code <-> test matrix from the *real* repository tree and fails
(exit 1) when an IMPLEMENTED requirement has no test, or when code/tests reference
a REQ that no spec declares (drift / scope creep).

Tag requirements anywhere in source and test files, e.g.:
    # REQ-002  (Python)        // REQ-002 (Go/TS/Java)
    def test_req_002_limit():  ...   # test names work too

A feature is only ENFORCED once it has real work (a task marked `done`, or any
code referencing one of its REQs). Pure spec/plan/tasks-stage features are reported
as "pending" and do not fail the build. Use --strict to enforce everything.

Usage:
    python scripts/trace.py                 # check whole repo
    python scripts/trace.py --feature 001-api-rate-limit
    python scripts/trace.py --strict        # enforce pending features too
    python scripts/trace.py --report-only   # never exit non-zero
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_RE = re.compile(r"REQ-\d{3,}")

# Directories that are pipeline infrastructure, not project code.
SKIP_DIRS = {
    ".git", "specs", "templates", "flow", "memory", "_build", "scripts", "docs",
    ".claude", ".cursor", ".agents", ".github", "node_modules", ".venv", "venv",
    "dist", "build", "__pycache__", ".pytest_cache", ".mypy_cache", "target",
}
CODE_EXT = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rb", ".rs",
            ".kt", ".cs", ".php", ".swift", ".scala", ".c", ".cpp", ".h", ".hpp"}


def is_test_file(p: Path) -> bool:
    n = p.name.lower()
    parts = {x.lower() for x in p.parts}
    return (
        n.startswith("test_") or n.endswith("_test" + p.suffix)
        or ".test." in n or ".spec." in n
        or "tests" in parts or "test" in parts or "__tests__" in parts
    )


def parse_spec(spec: Path):
    """Return (status, set_of_req_ids) declared in a spec.md."""
    status, reqs = "draft", set()
    in_reqs = False
    for line in spec.read_text(encoding="utf-8", errors="ignore").splitlines():
        low = line.lower()
        if low.startswith("- **status:**") or low.startswith("**status:**"):
            status = low.split("status:**", 1)[1].strip(" |").split()[0] if "status:**" in low else status
        if low.startswith("## requirements"):
            in_reqs = True
            continue
        if in_reqs and line.startswith("## "):
            in_reqs = False
        if in_reqs:
            reqs.update(REQ_RE.findall(line))
    return status, reqs


def parse_tasks(tasks: Path):
    """Return list of (req_ids:set, status:str) per task row, and any-done flag."""
    rows = []
    for line in tasks.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip().startswith("| T-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        reqs = set(REQ_RE.findall(line))
        status = ""
        for c in cells:
            if c.lower() in {"todo", "doing", "done", "blocked", "stale"}:
                status = c.lower()
        rows.append((reqs, status))
    return rows


def scan_markers():
    """Map REQ id -> {'code': set(paths), 'test': set(paths)} across project code."""
    found: dict[str, dict[str, set]] = {}
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix not in CODE_EXT:
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        ids = set(REQ_RE.findall(text))
        if not ids:
            continue
        kind = "test" if is_test_file(p) else "code"
        for rid in ids:
            found.setdefault(rid, {"code": set(), "test": set()})[kind].add(
                str(p.relative_to(ROOT))
            )
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--feature", help="only this feature folder name")
    ap.add_argument("--strict", action="store_true", help="enforce pending features too")
    ap.add_argument("--report-only", action="store_true", help="never exit non-zero")
    args = ap.parse_args()

    specs_dir = ROOT / "specs"
    if not specs_dir.exists():
        print("no specs/ directory found — nothing to check")
        return 0

    markers = scan_markers()
    all_declared: set[str] = set()
    errors: list[str] = []
    warnings: list[str] = []

    feature_dirs = sorted(d for d in specs_dir.iterdir() if d.is_dir())
    if args.feature:
        feature_dirs = [d for d in feature_dirs if d.name == args.feature]

    for fdir in feature_dirs:
        spec = fdir / "spec.md"
        if not spec.exists():
            continue
        status, declared = parse_spec(spec)
        all_declared |= declared
        tasks_path = fdir / "tasks.md"
        task_rows = parse_tasks(tasks_path) if tasks_path.exists() else []
        task_reqs = set().union(*[r for r, _ in task_rows]) if task_rows else set()
        any_done = any(s == "done" for _, s in task_rows)
        code_touched = any(rid in markers for rid in declared)
        implemented = any_done or code_touched
        enforce = (implemented or args.strict) and status == "approved"

        print(f"\n=== {fdir.name}  (status: {status}, "
              f"{'implemented' if implemented else 'pending'}) ===")
        print(f"{'REQ':<10}{'task':<6}{'code':<6}{'test':<6}")
        for rid in sorted(declared):
            has_task = "✓" if rid in task_reqs else "·"
            has_code = "✓" if markers.get(rid, {}).get("code") else "·"
            has_test = "✓" if markers.get(rid, {}).get("test") else "·"
            print(f"{rid:<10}{has_task:<6}{has_code:<6}{has_test:<6}")

            if tasks_path.exists() and rid not in task_reqs:
                msg = f"{fdir.name}: {rid} declared but no task covers it"
                (errors if enforce else warnings).append(msg)
            if enforce:
                if not markers.get(rid, {}).get("test"):
                    errors.append(f"{fdir.name}: {rid} has no test (Article V)")
                if not markers.get(rid, {}).get("code"):
                    warnings.append(f"{fdir.name}: {rid} approved but not implemented yet")

    # Unknown REQ markers in code/tests that no spec declares = drift.
    for rid, where in markers.items():
        if rid not in all_declared:
            locs = ", ".join(sorted(where["code"] | where["test"]))
            errors.append(f"unknown {rid} referenced in code but declared in no spec: {locs}")

    print("\n" + "-" * 60)
    for w in warnings:
        print(f"⚠️  {w}")
    for e in errors:
        print(f"❌ {e}")
    if not errors and not warnings:
        print("✅ traceability clean")
    elif not errors:
        print("✅ no blocking violations (warnings only)")

    if errors and not args.report_only:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
