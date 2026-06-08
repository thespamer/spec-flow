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
