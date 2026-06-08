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

## Article IX — The spec is amended, never bypassed
When implementation reveals the spec is wrong or incomplete, work **stops**. You do
not silently edit code around the spec. You run the **amendment protocol**: change
the affected `REQ`, log it in the spec changelog, set the spec back to
`needs-approval`, get re-approval at the gate, then regenerate only the impacted
tasks. Code and spec move together or not at all. (See `flow/sync.md`.)

## Article X — Durable memory lives in `context.md`
Every feature keeps a `context.md` decision journal: constraints, assumptions,
rejected alternatives, and a dated decision log. It is updated **as work happens**,
not reconstructed afterward. Any agent starting a fresh session re-reads
`spec.md` + `plan.md` + `tasks.md` (status) + `context.md` before acting. This is
what prevents "why was it built this way?" amnesia two weeks later.

## Article XI — Traceability is machine-verified
Rastreability is not an honor system. Requirements are tagged in code and tests
(`REQ-xxx`), and `scripts/trace.py` builds the matrix from the *real* tree and
**fails CI** when an implemented requirement has no test, or code references a
requirement no spec declares. A spec only "counts" while the build proves it is in
sync with what ships.
