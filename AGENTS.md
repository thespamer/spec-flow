# AGENTS.md

Spec-driven development pipeline for this repository. **Any** coding agent
(Claude Code, OpenAI Codex, Cursor, GitHub Copilot in VS Code, Google Antigravity)
should follow the workflow below. This file is the cross-tool source of truth;
tool-specific files (`CLAUDE.md`, `.cursor/`, `.agents/`, `.github/`) only point back here.

## The pipeline

```
constitution ──▶ /specify ──▶ /plan ──▶ /tasks ──▶ /implement ──▶ /verify
   (always)       spec.md      plan.md    tasks.md     code+commits   report
                     │            │           │             │
                   GATE         GATE        GATE            │   ◀── human approval
                     ▲                                      │
                     └──────── /sync (reverse path) ◀───────┘
              amend spec when code drifts; never bypass it (Article IX)
```

The procedure for each phase lives in `flow/<phase>.md` and is the single
definition every tool reuses:

| Command | Procedure | What it produces |
|---------|-----------|------------------|
| `/specify`   | `flow/specify.md`   | `specs/<NNN-slug>/spec.md` (`--amend` to change a REQ) |
| `/plan`      | `flow/plan.md`      | `specs/<NNN-slug>/plan.md` |
| `/tasks`     | `flow/tasks.md`     | `specs/<NNN-slug>/tasks.md` (`--refresh` after an amend) |
| `/implement` | `flow/implement.md` | tested code, one commit per task |
| `/verify`    | `flow/verify.md`    | traceability report |
| `/sync`      | `flow/sync.md`      | drift report + reconciliation actions |

Each feature also keeps a `context.md` decision journal (durable memory, Article X).

## Keeping spec & code in sync

The spec only earns its keep while it matches what ships. Two mechanisms enforce this
instead of leaving it to discipline:

- **Machine-checked traceability.** Tag `REQ-xxx` in code and tests; `scripts/trace.py`
  builds the matrix from the real tree and **fails CI** on uncovered or unknown REQs.
- **Amendment protocol (Article IX).** When implementation contradicts the spec, stop
  and run `/specify --amend` → `/tasks --refresh` → re-approve → resume. The spec is
  amended, never bypassed. Use `/sync` to detect drift at any time.

## Constraints (read `memory/constitution.md` for the full text)

- **Do** write a spec before any code; resolve ambiguity with the human.
- **Do** keep each task to one small, reversible, independently committed change.
- **Do** write the failing test first (Red → Green → Refactor).
- **Do** trace every requirement to a test and every test to a requirement ID, and
  tag `REQ-xxx` in code/tests so `scripts/trace.py` can verify it.
- **Do** keep `context.md` current — log decisions and constraints as you work.
- **Don't** advance past a gate (`spec→plan`, `plan→tasks`, `tasks→implement`)
  without explicit human approval (`python scripts/check_gate.py` enforces it).
- **Don't** let a worker touch files outside its task's declared scope.
- **Don't** silently edit an approved spec/plan from a later phase — run `/specify --amend`.

## Commands

- **Test:** `<fill in your project's test command>`
- **Lint / typecheck:** `<fill in>`
- **Build:** `<fill in>`
- **Traceability check:** `python scripts/trace.py` (run in CI)
- **Approval gate:** `python scripts/check_gate.py specs/<feature>`

## Conventions

- Feature folders: `specs/NNN-slug/` with `spec.md`, `plan.md`, `tasks.md`.
- Requirement IDs `REQ-xxx`; task IDs `T-xxx`; commits reference both, e.g.
  `feat(T-003): add rate limiter [REQ-007]`.
