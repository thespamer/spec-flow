# spec-flow

A **spec-driven development pipeline** that runs the same way across **Claude Code,
OpenAI Codex, Cursor, GitHub Copilot (VS Code), and Google Antigravity**.

It turns a feature idea into shipped code through five gated phases —
`specify → plan → tasks → implement → verify` — so an AI agent behaves like a
disciplined engineering team instead of an over-eager solo coder.

```
constitution ──▶ /specify ──▶ /plan ──▶ /tasks ──▶ /implement ──▶ /verify
   (always)       spec.md      plan.md    tasks.md     code+commits   report
                     │            │           │             │
                   GATE         GATE        GATE            │  ◀── you approve to advance
                     ▲                                      │
                     └──────────── /sync (reverse) ◀────────┘
              when code drifts, amend the spec — never bypass it
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
├── memory/constitution.md    # always-on principles (11 articles)
├── flow/                     # canonical phase procedures (edit these)
│   ├── specify.md  plan.md  tasks.md  implement.md  verify.md  sync.md
├── templates/                # spec / plan / tasks / context templates (EARS)
├── specs/001-api-rate-limit/ # worked example (spec + plan + tasks + context journal)
├── scripts/                  # trace.py (CI traceability) + check_gate.py (approval gate)
├── docs/context-drift.md     # the anti-drift chapter — read this
├── .claude/                  # Claude Code: skills/ + agents/ + settings.json (hooks)
├── .cursor/                  # Cursor: rules/ + commands/
├── .agents/                  # Antigravity: rules/ + workflows/
└── .github/                  # VS Code/Copilot: copilot-instructions.md + prompts/ + workflows/ci
```

## Installing it into your project

**Everything goes at the root of the project you open in your editor.** These folders
are not optional extras to scatter around — each tool only finds its config when the
folder sits at the repository root. Copy the *contents* of this repo into your project
root so it looks like this:

```
your-project/
├── AGENTS.md              # read by Codex, Cursor, Copilot, Antigravity
├── CLAUDE.md  GEMINI.md   # tool pointers (must be at root)
├── memory/                # constitution.md
├── flow/                  # the 5 phase procedures
├── templates/             # spec / plan / tasks templates
├── specs/                 # your features live here
├── .claude/               # Claude Code      → skills/ + agents/ + settings.json
├── .cursor/               # Cursor           → rules/ + commands/
├── .agents/               # Antigravity      → rules/ + workflows/
└── .github/               # VS Code/Copilot  → copilot-instructions.md + prompts/
```

Which tool reads which folder, and how you trigger a phase:

| Tool | Reads from (at root) | Invoke a phase |
|------|----------------------|----------------|
| Claude Code | `.claude/skills/`, `.claude/agents/` | type `/specify` in chat |
| OpenAI Codex | `AGENTS.md` (+ `.claude/skills/`) | ask it to run `/specify` |
| Cursor | `.cursor/rules/`, `.cursor/commands/` | type `/specify` |
| GitHub Copilot (VS Code) | `.github/copilot-instructions.md`, `.github/prompts/` | type `/specify` |
| Google Antigravity | `.agents/rules/`, `.agents/workflows/` | type `/specify` |

The shared parts (`AGENTS.md`, `flow/`, `memory/`, `templates/`, `specs/`) are used by
**every** tool. The dot-folders are the thin per-tool adapters. Keep all of them — a
single project can be opened by teammates using different tools.

### ⚠️ Watch out — these are hidden folders

`.claude`, `.cursor`, `.agents`, and `.github` start with a dot, so they are
**hidden files**. Two things go wrong most often when you unzip:

1. **Nesting.** Extracting `spec-flow.zip` may create a `spec-flow/` parent folder. You
   want the *contents* at your root, not a `spec-flow/` subfolder. Move them up one level.
2. **Dotfiles skipped.** Some unzip tools / file managers silently skip files that start
   with a dot. Confirm the dot-folders actually arrived.

Verify from your project root before you start:

```bash
ls -la .claude/skills    # must list: specify  plan  tasks  implement  verify
ls -la                   # confirm AGENTS.md, flow/, memory/, specs/ are here too
```

If the five skill folders show up, open your editor at this root and type `/specify`.
If the editor was already open, **restart the session** so it reloads the new config.

## Running the phases

Once installed, fill in your project's real test / lint / build commands under
**AGENTS.md → Commands**, then drive the work from your editor's agent chat.

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

## Adding a new feature in practice

This is the day-to-day loop. The unit of work is a **feature folder** under
`specs/` — *not* a task. Tasks are **rows inside** that feature's `tasks.md`, not
subfolders.

```
specs/
└── 002-user-auth/        # one folder per feature (the NNN- prefix just orders them)
    ├── spec.md           # what & why  — requirements REQ-001, REQ-002, …
    ├── plan.md           # how         — architecture & decisions
    └── tasks.md          # the tasks   — rows T-001, T-002, … (not subfolders)
```

You almost never create these files by hand — you run the phases and let each one
write the next artifact into the folder. There are two ways to start.

### Path A — let the pipeline drive it (recommended)

You don't even create the folder yourself. In your editor's agent chat:

1. **`/specify`** → describe the feature, e.g. *"login with email + password, lock
   the account after 5 failed attempts"*. The agent picks the next number (`002-`),
   creates `specs/002-user-auth/`, writes `spec.md` in EARS format, and **stops** for
   your review.
2. Read `spec.md`, fix anything, then say *"approved"*.
3. **`/plan`** → reads the approved spec, writes `plan.md`, stops.
4. **`/tasks`** → reads the plan, writes `tasks.md` (the task DAG), stops.
5. **`/implement`** → works the tasks one at a time: failing test → code → refactor →
   one commit per task.
6. **`/verify`** → builds the REQ↔test matrix and confirms nothing is uncovered.

You approve at each of the three gates; the agent never jumps a gate on its own.

### Path B — hand-write the spec, let the pipeline do the rest

Useful when you already know the requirements:

```bash
mkdir -p specs/002-user-auth
cp templates/spec.template.md specs/002-user-auth/spec.md
# edit spec.md — fill in REQ-001, REQ-002, … each with acceptance criteria
```

Then point the agent at it: *"run /plan for specs/002-user-auth/spec.md"*. From here
it is identical to Path A (plan → tasks → implement → verify).

### Adding a task to an existing feature

A task is **a row, not a folder**. Open that feature's `tasks.md` and add a line:

```
| T-006 | Add password-strength check | REQ-004 | auth/validators | T-002 | test_validators.py | todo |
```

Give it an ID, the `REQ` it serves, its file scope, what it `depends_on`, and the
test that proves it. `/implement` then picks it up in dependency order. (You can
also just ask `/tasks` to regenerate the list from the plan.)

### The one rule that makes it all work

Every requirement in `spec.md` needs a stable **`REQ-xxx` ID**. That ID is the thread
`/plan` maps to components and `/verify` traces to tests. A spec written as loose
prose without IDs will still run, but you lose the traceability that is the whole
point (Constitution, Article V). When unsure of the shape, copy
`specs/001-api-rate-limit/` — it is the reference mould.

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
| **sync** | drift report; reconciles spec ↔ shipped code (reverse path) | run anytime |

## Keeping spec & code in sync (the anti-drift chapter)

> A spec only earns its keep while it stays synced with what ships. The moment code
> edits bypass it, the drift and the "why was this built this way?" amnesia come back.

That problem — context drift — gets its own chapter: **[docs/context-drift.md](./docs/context-drift.md)**.
The short version is that spec-flow turns *discipline* into *mechanism* with four parts:

1. **Machine-checked traceability.** You tag `REQ-xxx` in code and tests;
   `scripts/trace.py` builds the matrix from the real tree and **fails CI**
   (`.github/workflows/spec-flow.yml`) if an implemented requirement has no test, or
   code references a `REQ` no spec declares.
2. **The reverse path — `/sync`.** Detects drift and classifies it (in-sync /
   spec-ahead / code-ahead), proposing a concrete reconciliation for each gap.
3. **The amendment protocol.** When implementation contradicts the spec you don't
   patch around it: `/specify --amend` → `/tasks --refresh` → re-approve → resume.
   The spec is amended, never bypassed (Constitution, Article IX).
4. **A decision journal per feature.** `context.md` is durable memory — constraints,
   rejected alternatives, a dated decision log — read at the start of every session so
   the "why" survives even when no one remembers it two weeks later (Article X).

There is also a real approval gate: `python scripts/check_gate.py specs/<feature>`
refuses to let `/implement` start until `spec.md` and `plan.md` are `approved`.

## Extending

- Add a phase: create `flow/<name>.md`, then mirror a thin wrapper in each tool
  folder (or run `_build/build_adapters.py` after adding it to the `PHASES` list).
- Change a phase's behaviour: edit only `flow/<phase>.md`.
- Add hard gates: extend `.claude/settings.json` hooks (e.g. block edits until a
  spec is marked approved) and the equivalent in your other tools.

## License

Apache License 2.0 — see [LICENSE](./LICENSE).
