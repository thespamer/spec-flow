#!/usr/bin/env python3
"""spec-flow approval gate.

Refuses to let a feature advance to implementation until both spec.md and plan.md
are marked `Status: approved`. Wire it into /implement (it runs this first) and,
optionally, a pre-commit or CI step.

Usage:
    python scripts/check_gate.py specs/001-api-rate-limit
    python scripts/check_gate.py specs/001-api-rate-limit --require spec plan tasks
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path


def status_of(md: Path) -> str | None:
    if not md.exists():
        return None
    for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
        low = line.lower().strip()
        if low.startswith("- **status:**") or low.startswith("**status:**"):
            return low.split("status:**", 1)[1].strip(" |").split()[0]
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("feature", help="path to the feature folder, e.g. specs/001-...")
    ap.add_argument("--require", nargs="+", default=["spec", "plan"],
                    help="artifacts that must be approved (default: spec plan)")
    args = ap.parse_args()

    fdir = Path(args.feature)
    if not fdir.exists():
        print(f"❌ {fdir} does not exist")
        return 1

    blocked = False
    for art in args.require:
        st = status_of(fdir / f"{art}.md")
        if st is None:
            print(f"❌ {art}.md missing — cannot pass the gate")
            blocked = True
        elif st != "approved":
            print(f"❌ {art}.md is '{st}', must be 'approved' before implementing")
            blocked = True
        else:
            print(f"✅ {art}.md approved")

    if blocked:
        print("\nGate CLOSED — get human approval first (Constitution, Article VII).")
        return 1
    print("\nGate OPEN — cleared to implement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
