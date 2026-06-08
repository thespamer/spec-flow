# Phase 1 — Specify

**Goal:** turn a raw idea into a rigorous, testable `spec.md`. Output *what* and
*why*, never *how*.

**Inputs:** the user's feature idea, plus `memory/constitution.md`.
**Output:** `specs/<NNN-feature-slug>/spec.md` (use `templates/spec.template.md`).
**Gate:** pause for explicit human approval before Phase 2.

## Procedure
1. Read `memory/constitution.md`. If the idea conflicts with any article, raise it now.
2. Pick the next feature number `NNN` (zero-padded) and a short slug. Create the
   folder `specs/<NNN-slug>/`.
3. Interview the human about anything ambiguous: actors, triggers, success
   criteria, edge cases, non-goals, constraints. Ask the **smallest** set of
   questions that removes real ambiguity — do not interrogate.
4. Write requirements in **EARS** syntax (Easy Approach to Requirements Syntax):
   - Ubiquitous: `The <system> shall <response>.`
   - Event-driven: `When <trigger>, the <system> shall <response>.`
   - State-driven: `While <state>, the <system> shall <response>.`
   - Unwanted: `If <condition>, then the <system> shall <response>.`
   - Optional: `Where <feature is included>, the <system> shall <response>.`
   Give every requirement a stable ID (`REQ-001`, `REQ-002`, …).
5. For each requirement add **acceptance criteria** phrased so they can become tests.
6. Fill the `## Non-goals` and `## Open questions` sections. Mark unresolved items
   with `[NEEDS CLARIFICATION: …]` rather than inventing an answer.
7. Save the file. Summarise the spec in 3–5 bullets and **stop**: ask the human to
   review and approve, or list the `[NEEDS CLARIFICATION]` items blocking approval.

## Amendment mode (`/specify --amend <feature>`)
Use this when a *later* phase discovers the spec is wrong or incomplete (Article IX).
Do **not** rewrite the whole spec:
1. Edit only the affected `REQ-xxx` (or add a new one with the next ID — never reuse).
2. Append a row to the spec's `## Changelog`: date, what changed, why, who triggered it.
3. Set `Status: needs-approval` and stop for re-approval at the gate.
4. After approval, hand off to `/tasks --refresh` so only the impacted tasks regenerate,
   then resume `/implement`. Record the amendment in the feature's `context.md`.

## Definition of done
- Every requirement is EARS-formatted, ID'd, and has acceptance criteria.
- No `[NEEDS CLARIFICATION]` markers remain (or they are explicitly accepted by the human).
- Non-goals are stated. The human has approved.
