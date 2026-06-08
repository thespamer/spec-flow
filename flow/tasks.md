# Phase 3 — Tasks

**Goal:** decompose an approved `plan.md` into an ordered, dependency-aware task
list where each task is small, testable, and independently committable.

**Inputs:** approved `specs/<feature>/plan.md`, the spec, the constitution.
**Output:** `specs/<feature>/tasks.md` (use `templates/tasks.template.md`).
**Gate:** pause for explicit human approval before Phase 4.

## Procedure
1. Confirm `plan.md` is approved.
2. Break the plan into tasks. Each task must:
   - have a stable ID (`T-001`, `T-002`, …);
   - reference the `REQ-xxx` it advances and the plan component it touches;
   - be doable in a single focused commit (Article IV);
   - name the test(s) that prove it (Article III).
3. Declare **dependencies** between tasks (`depends_on: [T-001]`). Order so that
   independent tasks can run in parallel and blocked tasks come after their blockers.
4. Front-load a task that writes the failing tests for the slice, when that makes
   the TDD loop cleaner.
5. Add a final task that runs Phase 5 (verify) for the feature.
6. Save the file. Summarise the task graph (count, parallelizable set, critical
   path) and **stop** for human approval.

## Refresh mode (`/tasks --refresh <feature>`)
Triggered after a spec amendment (Article IX). Do **not** rebuild the whole list:
1. Diff the amended spec against the current tasks.
2. Mark tasks tied to a changed `REQ` as `stale`; add new tasks for new requirements.
3. Leave untouched tasks (and their commits) exactly as they are.
4. Summarise what changed and stop for approval before re-running `/implement`.

## Definition of done
- Every task is ID'd, traces to a REQ and a plan component, and names its tests.
- Dependencies form a valid DAG (no cycles). The human has approved.
