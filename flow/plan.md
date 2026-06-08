# Phase 2 — Plan

**Goal:** turn an approved `spec.md` into a `plan.md` that owns every *how*
decision. No code yet.

**Inputs:** approved `specs/<feature>/spec.md`, `memory/constitution.md`.
**Output:** `specs/<feature>/plan.md` (use `templates/plan.template.md`).
**Gate:** pause for explicit human approval before Phase 3.

## Procedure
1. Confirm `spec.md` is approved and free of `[NEEDS CLARIFICATION]`. If not, go back.
2. Survey the existing codebase before proposing anything: language, framework,
   conventions, neighbouring modules, test setup. Reuse existing patterns over
   inventing new ones.
3. Choose an architecture that satisfies the spec with the least new surface area.
   Document the **data flow**, the **components** touched/created, and the
   **interfaces/contracts** between them.
4. Record every significant decision as a short ADR-style entry: *decision*,
   *alternatives considered*, *why this one*. Tie each back to the REQ IDs it serves.
5. Call out risks, migrations, rollout/rollback, and observability needs.
6. Map each `REQ-xxx` to the component(s) that will satisfy it, so nothing is dropped.
7. Save the file. Summarise the approach and **stop** for human approval.

## Definition of done
- Every `REQ-xxx` from the spec maps to at least one component in the plan.
- Tech choices are justified against alternatives and the constitution.
- Risks, rollback, and test strategy are explicit. The human has approved.
