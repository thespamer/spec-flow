# Phase 5 — Verify

**Goal:** prove the implementation satisfies the spec, and surface any gap.

**Inputs:** the spec, plan, tasks, and the implemented code + tests.
**Output:** a verification report (and, if gaps exist, new tasks in `tasks.md`).

## Procedure
1. Build a **traceability matrix**: for every `REQ-xxx`, list the test(s) that
   cover it and the task(s)/commit(s) that implemented it.
2. Flag any requirement with **no** covering test (Article V violation) and any
   test that maps to **no** requirement (scope creep).
3. Run the full test suite, lint, and typecheck. Record results.
4. Re-read each acceptance criterion in the spec and confirm a test asserts it.
5. Check the constitution: small commits? human gates respected? context isolation
   honoured?
6. Write the report: ✅ covered, ⚠️ partial, ❌ missing. For every ❌/⚠️, create a
   follow-up task rather than hand-waving.
7. **Stop** and present the report. Do not declare the feature done while any
   `REQ` is uncovered.

## Definition of done
- Traceability matrix is complete; no uncovered REQ remains unaddressed.
- Full suite green. Report delivered to the human.
