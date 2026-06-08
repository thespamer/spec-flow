# Phase 4 — Implement

**Goal:** execute the approved task list. You act as the **tech lead /
orchestrator**; each task is delegated to an isolated worker so context stays clean.

**Inputs:** approved `specs/<feature>/tasks.md`, the plan, the spec, the constitution.
**Output:** working, tested code; one commit per task.

## Orchestration loop
For each task in dependency order (parallelize independent tasks where the tool allows):

1. **Dispatch in isolation.** Hand the single task to a worker with a *clean*
   context (in Claude Code: the `developer` subagent / a forked context; in
   Antigravity: a worker agent; elsewhere: a fresh sub-task). Give it only what it
   needs: the task, its REQs, the relevant plan section, and the files in scope.
2. **TDD.** The worker writes the failing test first, then the minimal code to pass,
   then refactors. It does **not** touch files outside the task's declared scope.
3. **Verify locally.** Run the task's tests plus lint/typecheck. If red, fix within
   the task; if blocked, stop and report — do not expand scope.
4. **Commit.** One conventional commit referencing the task and REQ
   (e.g. `feat(T-003): add rate limiter [REQ-007]`). Then continue to the next task.
5. **Log blockers.** Anything discovered but out of scope is recorded as a new
   task in `tasks.md`, not fixed inline.

## Rules
- Never start a task whose `depends_on` set is unmet.
- Never edit the spec or plan from here; if reality contradicts them, stop and
  kick back to Phase 1/2.
- Keep `tasks.md` updated with status (`todo` / `doing` / `done` / `blocked`).

## Definition of done
- Every task is `done` with a passing test and its own commit, or explicitly `blocked`
  with a reason. Proceed to Phase 5.
