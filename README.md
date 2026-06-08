# spec-flow

A **spec-driven development pipeline** that runs the same way across **Claude Code,
OpenAI Codex, Cursor, GitHub Copilot (VS Code), and Google Antigravity**.

It turns a feature idea into shipped code through five gated phases —
`specify → plan → tasks → implement → verify` — so an AI agent behaves like a
disciplined engineering team instead of an over-eager solo coder.

```
constitution ──▶ /specify ──▶ /plan ──▶ /tasks ──▶ /implement ──▶ /verify
   (always)       spec.md      plan.md    tasks.md     code+commits   report
                     │            │           │
                   GATE         GATE        GATE   ◀── you approve before advancing
```

## Why this design

One source of truth, thin adapters per tool — the 2026 cross-tool consensus:

- **`AGENTS.md`** is read natively by Codex, Cursor, Copilot, and Antigravity.
- **`flow/<phase>.md`** holds the canonical procedure for each phase. Every tool
  reuses it, so you edit a phase in exactly one place.
- **`memory/constitution.md`** holds the non-negotiable principles enforced in
  every phase.
- Tool folders (`.claude/`, `.cursor/`, `.agents/`, `.github/`) contain only thin
  wrappers that point back to `flow/`.

## Layout

```
spec-flow/
├── AGENTS.md                 # universal source of truth (Codex/Cursor/Copilot/Antigravity)
├── CLAUDE.md  GEMINI.md      # thin tool pointers
├── memory/constitution.md    # always-on principles
├── flow/                     # canonical phase procedures (edit these)
│   ├── specify.md  plan.md  tasks.md  implement.md  verify.md
├── templates/                # spec / plan / tasks artifact templates (EARS)
├── specs/001-api-rate-limit/ # worked example (spec + plan + tasks)
├── .claude/                  # Claude Code: skills/ + agents/ + settings.json (hooks)
├── .cursor/                  # Cursor: rules/ + commands/
├── .agents/                  # Antigravity: rules/ + workflows/
└── .github/                  # VS Code/Copilot: copilot-instructions.md + prompts/
```

## Install & use

Drop these files into your project root (or keep this as a template repo and copy
the folders you need). Then, in **AGENTS.md → Commands**, fill in your project's
real test / lint / build commands.

### Claude Code
Skills auto-register from `.claude/skills/`. Run the phases as slash commands:
```
/specify   # idea → spec.md, then stops for your approval
/plan      # approved spec → plan.md
/tasks     # approved plan → tasks.md
/implement # executes tasks: one developer subagent + one commit per task
/verify    # traceability matrix + full suite
```
Side-effecting phases use `disable-model-invocation: true`, so Claude won't fire
them on its own — you invoke them. Phase work is delegated to the subagents in
`.claude/agents/` to keep context clean.

### OpenAI Codex
Codex reads `AGENTS.md` at the repo root automatically. Ask it to "run /specify
for <feature>" (or reference `flow/specify.md`). Codex CLI also reads the
`SKILL.md` files under `.claude/skills/` via the Agent Skills standard.

### Cursor
`.cursor/rules/spec-flow.mdc` is always applied. Invoke the phases with the
slash commands in `.cursor/commands/` (`/specify`, `/plan`, …). Cursor also reads
`AGENTS.md` as a fallback rule source.

### GitHub Copilot (VS Code)
`.github/copilot-instructions.md` is loaded automatically. Run phases via the
prompt files in `.github/prompts/` (type `/specify`, `/plan`, … in chat).

### Google Antigravity
`.agents/rules/spec-flow.md` is auto-loaded as project rules. Trigger phases with
the workflows in `.agents/workflows/` (`/specify`, `/plan`, …) in agent chat.
Antigravity also honours `AGENTS.md`.

## A full run (the included example)

`specs/001-api-rate-limit/` shows the artifacts for a real feature — per-client
API rate limiting — already taken through specify → plan → tasks. Read those three
files top to bottom to see the EARS requirements, the ADR-style plan, and the
dependency-aware task DAG before you start your own feature.

## The phases

| Phase | Produces | Gate |
|-------|----------|------|
| **specify** | `spec.md` — EARS requirements + acceptance criteria | approve before plan |
| **plan** | `plan.md` — architecture, decisions, REQ→component map | approve before tasks |
| **tasks** | `tasks.md` — small, testable, dependency-aware tasks | approve before implement |
| **implement** | tested code, one commit per task (TDD, isolated workers) | — |
| **verify** | traceability matrix; every REQ covered by a test | done |

## Extending

- Add a phase: create `flow/<name>.md`, then mirror a thin wrapper in each tool
  folder (or run `_build/build_adapters.py` after adding it to the `PHASES` list).
- Change a phase's behaviour: edit only `flow/<phase>.md`.
- Add hard gates: extend `.claude/settings.json` hooks (e.g. block edits until a
  spec is marked approved) and the equivalent in your other tools.

## License

Apache License 2.0 — see [LICENSE](./LICENSE).
