#!/usr/bin/env python3
"""Generate AGENTS.md (source of truth) and the thin per-tool adapters.

Every adapter points back to flow/<phase>.md so there is exactly one place to
edit a phase. Adapters differ only in the wrapper each tool expects.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PHASES = [
    ("specify", "Phase 1 · Idea → spec.md (EARS requirements). Pauses for approval."),
    ("plan",    "Phase 2 · Approved spec → plan.md (architecture/decisions). Pauses for approval."),
    ("tasks",   "Phase 3 · Approved plan → tasks.md (ordered, dependency-aware). Pauses for approval."),
    ("implement","Phase 4 · Execute tasks; one isolated worker + one commit per task (TDD)."),
    ("verify",  "Phase 5 · Traceability matrix spec↔tests↔code; full suite green."),
]
SIDE_EFFECTING = {"specify", "plan", "tasks", "implement"}  # invoke explicitly


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.lstrip("\n"), encoding="utf-8")
    print(f"  wrote {rel}")


# ==========================================================================
# AGENTS.md — universal source of truth (Codex, Cursor, Copilot, Antigravity)
# ==========================================================================
write("AGENTS.md", r"""
# AGENTS.md

Spec-driven development pipeline for this repository. **Any** coding agent
(Claude Code, OpenAI Codex, Cursor, GitHub Copilot in VS Code, Google Antigravity)
should follow the workflow below. This file is the cross-tool source of truth;
tool-specific files (`CLAUDE.md`, `.cursor/`, `.agents/`, `.github/`) only point back here.

## The pipeline

```
constitution ──▶ /specify ──▶ /plan ──▶ /tasks ──▶ /implement ──▶ /verify
   (always)       spec.md      plan.md    tasks.md     code+commits   report
                     │            │           │
                   GATE         GATE        GATE   ◀── human approval required
```

The procedure for each phase lives in `flow/<phase>.md` and is the single
definition every tool reuses:

| Command | Procedure | What it produces |
|---------|-----------|------------------|
| `/specify`   | `flow/specify.md`   | `specs/<NNN-slug>/spec.md` |
| `/plan`      | `flow/plan.md`      | `specs/<NNN-slug>/plan.md` |
| `/tasks`     | `flow/tasks.md`     | `specs/<NNN-slug>/tasks.md` |
| `/implement` | `flow/implement.md` | tested code, one commit per task |
| `/verify`    | `flow/verify.md`    | traceability report |

## Constraints (read `memory/constitution.md` for the full text)

- **Do** write a spec before any code; resolve ambiguity with the human.
- **Do** keep each task to one small, reversible, independently committed change.
- **Do** write the failing test first (Red → Green → Refactor).
- **Do** trace every requirement to a test and every test to a requirement ID.
- **Don't** advance past a gate (`spec→plan`, `plan→tasks`, `tasks→implement`)
  without explicit human approval.
- **Don't** let a worker touch files outside its task's declared scope.
- **Don't** edit an approved spec/plan from a later phase — kick back instead.

## Commands

- **Test:** `<fill in your project's test command>`
- **Lint / typecheck:** `<fill in>`
- **Build:** `<fill in>`

## Conventions

- Feature folders: `specs/NNN-slug/` with `spec.md`, `plan.md`, `tasks.md`.
- Requirement IDs `REQ-xxx`; task IDs `T-xxx`; commits reference both, e.g.
  `feat(T-003): add rate limiter [REQ-007]`.
""")


# ==========================================================================
# Tool pointers
# ==========================================================================
write("CLAUDE.md", r"""
# CLAUDE.md

This project uses the spec-driven pipeline defined in **[AGENTS.md](./AGENTS.md)**
and **[memory/constitution.md](./memory/constitution.md)**. Read both first.

Claude Code specifics:
- Each phase is a **skill** in `.claude/skills/<phase>/` — run with `/specify`,
  `/plan`, `/tasks`, `/implement`, `/verify`. Side-effecting phases have
  `disable-model-invocation: true`, so they only run when you call them.
- Phase work is delegated to **subagents** in `.claude/agents/`
  (`spec-writer`, `architect`, `task-decomposer`, `developer`, `reviewer`).
- Hooks in `.claude/settings.json` run lint/tests after edits.
- The canonical procedure for every phase is still `flow/<phase>.md` — the skill
  is a thin wrapper. Edit `flow/*.md`, not the wrappers.
""")

write("GEMINI.md", r"""
# GEMINI.md

This project uses the spec-driven pipeline defined in **[AGENTS.md](./AGENTS.md)**
and **[memory/constitution.md](./memory/constitution.md)**. Follow those.

Gemini CLI / Google Antigravity specifics:
- Behaviour rules live in `.agents/rules/spec-flow.md` (auto-loaded).
- Phase commands are workflows in `.agents/workflows/<phase>.md`, triggered with
  `/specify`, `/plan`, `/tasks`, `/implement`, `/verify` in agent chat.
- The canonical procedure for every phase is `flow/<phase>.md`.
""")


# ==========================================================================
# Claude Code — skills, agents, settings
# ==========================================================================
SKILL_AGENT = {
    "specify": "spec-writer",
    "plan": "architect",
    "tasks": "task-decomposer",
    "implement": "developer",
    "verify": "reviewer",
}
for phase, desc in PHASES:
    fm = [
        "---",
        f"name: {phase}",
        f'description: >-',
        f"  {desc}",
        f"  Use this whenever the user wants to {phase} a feature in the spec-driven",
        f"  pipeline, or types /{phase}. Part of the spec-flow workflow defined in AGENTS.md.",
    ]
    if phase in SIDE_EFFECTING:
        fm.append("disable-model-invocation: true")
    fm.append("---")
    frontmatter = "\n".join(fm)
    delegate = SKILL_AGENT[phase]
    body = f"""
# /{phase}

Execute **Phase** `{phase}` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/{phase}.md`](../../../flow/{phase}.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`{delegate}`** subagent in a forked context
   so the main thread stays clean (`/agents` → `{delegate}`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/{phase}.md`;
> edit that, not this.
"""
    write(f".claude/skills/{phase}/SKILL.md", frontmatter + "\n" + body)

# subagents
AGENTS_DEF = {
    "spec-writer": (
        "Requirements analyst. Turns ideas into EARS-formatted, testable specs and "
        "interrogates ambiguity.",
        "Read, Grep, Glob, Write",
        "You are a meticulous requirements analyst. Follow `flow/specify.md`. You write "
        "*what* and *why*, never *how*. You prefer asking one sharp clarifying question "
        "over inventing an answer, and you mark unknowns with [NEEDS CLARIFICATION]."
    ),
    "architect": (
        "Software architect. Turns approved specs into plans that own all *how* decisions.",
        "Read, Grep, Glob, Write",
        "You are a pragmatic software architect. Follow `flow/plan.md`. You survey the "
        "existing codebase before proposing anything, reuse patterns over inventing them, "
        "minimise new surface area, and justify each decision against alternatives and the "
        "constitution. You write no production code."
    ),
    "task-decomposer": (
        "Delivery planner. Breaks plans into small, testable, dependency-aware tasks.",
        "Read, Grep, Glob, Write",
        "You decompose an approved plan into a task DAG. Follow `flow/tasks.md`. Every task "
        "is one commit, names its tests, and traces to a REQ. You verify dependencies form a "
        "valid DAG with no cycles."
    ),
    "developer": (
        "TDD engineer. Implements exactly one task in an isolated context.",
        "Read, Grep, Glob, Write, Edit, Bash",
        "You implement a single assigned task and nothing else. Follow `flow/implement.md`. "
        "You write the failing test first, then the minimal code to pass, then refactor. You "
        "never touch files outside the task's declared scope. If blocked, you stop and report "
        "instead of expanding scope. You make one conventional commit referencing the task and REQ."
    ),
    "reviewer": (
        "Verification reviewer. Builds the traceability matrix and finds gaps.",
        "Read, Grep, Glob, Bash",
        "You verify that the implementation satisfies the spec. Follow `flow/verify.md`. You "
        "build a REQ↔test↔commit matrix, run the full suite, and flag every uncovered "
        "requirement and every test with no requirement. You do not write feature code; you "
        "create follow-up tasks for gaps."
    ),
}
for name, (desc, tools, prompt) in AGENTS_DEF.items():
    write(f".claude/agents/{name}.md", f"""---
name: {name}
description: {desc}
tools: {tools}
---

{prompt}

Always read `memory/constitution.md` and the relevant `flow/*.md` before acting.
""")

write(".claude/settings.json", r"""{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '[spec-flow] file changed — run your project test/lint command here (see AGENTS.md > Commands)'"
          }
        ]
      }
    ]
  }
}
""")


# ==========================================================================
# Cursor — always-on rule + slash commands
# ==========================================================================
write(".cursor/rules/spec-flow.mdc", r"""---
description: Spec-driven development pipeline — always applied.
alwaysApply: true
---

This repo follows the spec-driven pipeline in [AGENTS.md](mdc:AGENTS.md) and the
principles in [memory/constitution.md](mdc:memory/constitution.md).

Never write production code before an approved `spec.md` and `plan.md`. Use the
slash commands `/specify`, `/plan`, `/tasks`, `/implement`, `/verify`, each of
which follows the matching `flow/<phase>.md`. Stop at every human gate.
""")
for phase, desc in PHASES:
    write(f".cursor/commands/{phase}.md", f"""# /{phase}

{desc}

Follow the canonical procedure in `flow/{phase}.md` and obey
`memory/constitution.md`. Produce the phase's artifact, then stop at the human
gate — do not auto-advance.
""")


# ==========================================================================
# Antigravity (Google) — rules + workflows
# ==========================================================================
write(".agents/rules/spec-flow.md", r"""# Spec-flow rules

This repository follows the spec-driven pipeline in @/AGENTS.md and the
principles in @/memory/constitution.md (always in effect).

- No production code before an approved `spec.md` and `plan.md`.
- Each task is one small, reversible, tested, separately-committed change.
- Stop at every human gate: `spec→plan`, `plan→tasks`, `tasks→implement`.
- Workers operate only within their task's declared file scope.

Phase workflows: `/specify`, `/plan`, `/tasks`, `/implement`, `/verify`.
""")
for phase, desc in PHASES:
    write(f".agents/workflows/{phase}.md", f"""# /{phase}

{desc}

Steps:
1. Follow the canonical procedure in @/flow/{phase}.md.
2. Obey @/memory/constitution.md.
3. Save all artifacts back to the file system under `specs/<feature>/`.
4. Stop at the human gate for this phase; summarise and wait for approval.
""")


# ==========================================================================
# VS Code (GitHub Copilot) — instructions + prompt files
# ==========================================================================
write(".github/copilot-instructions.md", r"""# Copilot instructions

This repository follows the spec-driven pipeline in [AGENTS.md](../AGENTS.md) and
the principles in [memory/constitution.md](../memory/constitution.md). Read both.

Do not write production code before an approved `spec.md` and `plan.md`. Drive the
work with the prompt files in `.github/prompts/` (`/specify`, `/plan`, `/tasks`,
`/implement`, `/verify`), each of which follows the matching `flow/<phase>.md`.
Keep tasks small and test-first; stop at every human gate.
""")
for phase, desc in PHASES:
    write(f".github/prompts/{phase}.prompt.md", f"""---
mode: agent
description: "{desc}"
---

Execute phase `{phase}` of the spec-driven pipeline.

Follow the canonical procedure in [`flow/{phase}.md`](../../flow/{phase}.md) and
obey [`memory/constitution.md`](../../memory/constitution.md). Produce the phase's
artifact under `specs/<feature>/`, then stop at the human gate.
""")

print("adapters: done")
