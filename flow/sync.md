# Phase R — Sync (the reverse path)

**Goal:** detect and reconcile **drift** between what the spec says and what the
code actually does. This is the answer to "a spec only earns its keep while it stays
synced with what ships." Run it any time, and always before declaring a feature done.

**Inputs:** the spec/plan/tasks, the implemented code + tests, git history.
**Output:** a drift report; for each drift, a concrete reconciliation action.

## Three states
- **In sync** — every `REQ` has matching code + tests; no stray `REQ` markers. ✅
- **Spec ahead** — a `REQ` exists but code/tests don't implement it yet → it is just
  unstarted work; make sure a task covers it.
- **Code ahead** — code implements behaviour the spec doesn't describe, or references a
  `REQ` no spec declares → this is **drift**. Either the spec must be amended to
  capture the new intent, or the code is scope creep to remove.

## Procedure
1. Run `python scripts/trace.py` to build the matrix from the real tree (it lists
   uncovered REQs, untested REQs, and unknown `REQ` markers).
2. Compare git history against `tasks.md`: any commit touching feature code whose task
   is not `done`, or any `done` task with no commit, is drift.
3. Classify every gap into one of the three states above.
4. For each **code-ahead** drift, decide *with the human*:
   - intent was real → `/specify --amend` to capture it as a REQ, then `/tasks --refresh`;
   - it was scope creep → open a task to remove or gate it.
5. For each **spec-ahead** gap, ensure a task exists (or create one).
6. Update `context.md` with what drifted and how it was reconciled.
7. Present the report and **stop**. Do not auto-amend the spec without approval.

## Definition of done
- `scripts/trace.py` exits clean (no uncovered/unknown REQs for implemented work).
- Every drift is either reconciled or captured as an approved task. `context.md` updated.
