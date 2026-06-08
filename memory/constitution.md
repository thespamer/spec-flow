# Project Constitution

> The non-negotiable principles every agent obeys in **every** phase of the
> pipeline. When a request conflicts with the constitution, the constitution
> wins — surface the conflict to the human instead of silently working around it.

## Article I — Spec before code
No production code is written before an **approved** `spec.md`. Ambiguity is
resolved with the human, not by guessing. Each spec states *what* and *why*,
never *how*.

## Article II — Plan before tasks
No task list exists before an **approved** `plan.md`. The plan owns all
*how* decisions: architecture, data flow, tech choices, and trade-offs.

## Article III — Test-first
Every behavioural task starts from a failing test (Red → Green → Refactor).
Tests are the executable form of the spec's acceptance criteria.

## Article IV — Small, reversible steps
One task = one focused, independently reviewable change with its own commit.
If a task cannot be expressed in a single coherent commit, it is too big — split it.

## Article V — Traceability
Every requirement traces to at least one test, and every test traces back to a
requirement ID. Code with no requirement is scope creep; a requirement with no
test is unverified.

## Article VI — Context isolation
Long-running work is decomposed so each task runs in a clean context. State that
must survive across tasks lives in files under `specs/<feature>/`, never only in
the agent's head.

## Article VII — Human gates
Three gates require explicit human approval before the pipeline advances:
`spec → plan`, `plan → tasks`, `tasks → implement`. An agent never approves its
own artifact.

## Article VIII — Honesty about limits
Agents report blockers, missing context, and uncertainty plainly. A wrong answer
delivered confidently is worse than a flagged unknown.
