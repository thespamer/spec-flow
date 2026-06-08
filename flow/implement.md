# Phase 4 — Implement

**Goal:** execute the approved task list. You act as the **tech lead /
orchestrator**; each task is delegated to an isolated worker so context stays clean.

**Inputs:** approved `specs/<feature>/tasks.md`, the plan, the spec, the constitution.
**Output:** working, tested code; one commit per task.

## Before you start
1. **Gate check.** Confirm `spec.md` and `plan.md` both read `Status: approved`
   (or run `python scripts/check_gate.py specs/<feature>`). If not, stop — you are
   not cleared to implement.
2. **Resume context (Article X).** Re-read `spec.md`, `plan.md`, `tasks.md` (note
   each task's status), and `context.md` before touching code. Find the first task
   that is `todo` with all `depends_on` satisfied; that is where you start.

## Orchestration loop
For each task in dependency order (parallelize independent tasks where the tool allows):

1. **Dispatch in isolation.** Hand the single task to a worker with a *clean*
   context (in Claude Code: the `developer` subagent / a forked context; in
   Antigravity: a worker agent; elsewhere: a fresh sub-task). Give it only what it
   needs: the task, its REQs, the relevant plan section, and the files in scope.
2. **TDD.** The worker writes the failing test first, then the minimal code to pass,
   then refactors. It does **not** touch files outside the task's declared scope.
   **Tag traceability:** put the `REQ-xxx` ID in a comment beside the code that
   satisfies it and in the test (name or comment), so `scripts/trace.py` can see it.
3. **Verify locally.** Run the task's tests plus lint/typecheck. If red, fix within
   the task; if blocked, stop and report — do not expand scope.
4. **Commit.** One conventional commit referencing the task and REQ
   (e.g. `feat(T-003): add rate limiter [REQ-007]`). Record the commit SHA next to
   the task in `tasks.md` and flip its status to `done`. Then continue.
5. **Log blockers.** Anything discovered but out of scope is recorded as a new
   task in `tasks.md`, not fixed inline.

## When reality contradicts the spec (the reverse path — Article IX)
If implementation reveals the spec is wrong or incomplete, **do not patch around it**:
1. Stop the current task and write what you learned into `context.md`.
2. Run `/specify --amend <feature>` to fix the affected `REQ`, then `/tasks --refresh`.
3. Re-approve at the gate, then resume here. The spec and code move together.
Use `/sync` at any time to detect drift between what shipped and what the spec says.

## Rules
- Never start a task whose `depends_on` set is unmet.
- Never silently edit an approved spec/plan from here — use the amendment protocol above.
- Keep `tasks.md` status current (`todo` / `doing` / `done` / `blocked` / `stale`).
- Keep `context.md` current: log every non-obvious decision and constraint as you go.

## Definition of done
- Every task is `done` with a passing test and its own commit, or explicitly `blocked`
  with a reason. Proceed to Phase 5.
