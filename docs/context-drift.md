# Keeping spec & code in sync — the anti-drift chapter

> *"A spec only earns its keep while it stays synced with what ships. The moment code
> edits bypass it, the drift and the 'why was this built this way?' amnesia come back,
> and spec-first quietly becomes a big document up front."*

That critique is the whole reason this chapter exists. Writing a spec is the easy part.
Keeping it true to the running code, sprint after sprint, is where spec-driven
development usually dies. spec-flow's answer is to stop relying on discipline and make
sync a **mechanism** — something the build enforces and the workflow routes around.

---

## 1. The problem, concretely

Two failure modes, both familiar:

- **Context evaporates between sessions.** Two weeks later, even the person who shipped
  the feature can't recall the constraints they were working under. The "why" is gone.
- **Code quietly drifts from the spec.** Someone fixes a bug or adds a branch during
  implementation, never updates the spec, and now the spec lies. Every future reader
  trusts a document that no longer matches reality.

The naive fix — "just keep the spec updated" — is exactly the discipline that fails
under deadline pressure. So we don't ask for discipline. We wire in four mechanisms.

---

## 2. The three states of sync

At any moment, each requirement is in one of three states. `/sync` exists to find which:

| State | What it means | What you do |
|-------|---------------|-------------|
| **In sync** ✅ | REQ has matching code **and** tests; no stray markers | nothing |
| **Spec ahead** | REQ exists, code/tests don't implement it yet | it's just unstarted work — make sure a task covers it |
| **Code ahead** ⚠️ | code does something the spec doesn't describe, or references a `REQ` no spec declares | **drift** — either amend the spec to capture the intent, or remove the scope creep |

"Code ahead" is the dangerous one. It's where the spec starts lying.

---

## 3. The four mechanisms

### Mechanism 1 — Machine-checked traceability (`scripts/trace.py` + CI)

Traceability stops being an honor system. You tag requirements right in the code and
tests:

```python
# REQ-002: reject the 101st request in the window
if count > LIMIT:
    return Response(status_code=429)
```

```python
def test_req_002_rejects_over_limit():   # the REQ id in the test name is enough
    ...
```

`scripts/trace.py` walks the **real** repository tree, finds every `REQ-xxx` marker,
and builds the matrix. It **fails the build** (exit 1, wired into
`.github/workflows/spec-flow.yml`) when:

- an **implemented** requirement has no test → Article V violation;
- code or tests reference a `REQ` that **no spec declares** → drift / scope creep.

Crucially, it only *enforces* a feature once there's real work (a task marked `done`,
or code already referencing its REQs). A feature still at the spec/plan stage is
reported as "pending" and never breaks CI — so the gate is real without being a nag.

```bash
python scripts/trace.py                      # whole repo (what CI runs)
python scripts/trace.py --feature 001-...     # one feature
python scripts/trace.py --strict              # enforce pending features too
```

### Mechanism 2 — The reverse path (`/sync`)

The forward pipeline turns intent into code. `/sync` runs the other direction: it takes
the shipped code and asks *"does the spec still describe this?"* It runs `trace.py`,
compares git history against `tasks.md`, classifies every gap into the three states
above, and proposes a concrete reconciliation for each. It **never** rewrites the spec
on its own — it reports and stops at a gate.

Run it whenever you suspect drift, and always before declaring a feature done.

### Mechanism 3 — The amendment protocol (Article IX)

This is the answer to *"when something changes during implementation, does the spec get
regenerated, or is it left to discipline?"* — **neither.** It doesn't regenerate
everything (that throws away approved, committed work), and it isn't left to discipline
(that's what fails). Instead, a change follows a fixed route:

```
discover spec is wrong during /implement
        │
        ▼
1. STOP the task, write what you learned into context.md
2. /specify --amend <feature>   → edit only the affected REQ, append a Changelog row,
                                   set Status: needs-approval
3. human re-approves at the gate
4. /tasks --refresh <feature>   → mark tasks tied to the changed REQ as `stale`,
                                   add tasks for new REQs, leave the rest untouched
5. resume /implement
```

The spec is **amended, never bypassed**, and only the *impacted* tasks regenerate.
Spec and code move together or not at all.

### Mechanism 4 — The decision journal (`context.md`, Article X)

Every feature folder carries a `context.md` — durable memory that outlives any single
session. It holds the constraints, the assumptions, the **rejected** alternatives (so
nobody re-litigates them next month), and a dated decision log. It's updated *as work
happens*, and it's the first file any agent or teammate reads when resuming. Each `done`
task also records its commit SHA in `tasks.md`, so a fresh session knows exactly where
it left off.

This is what kills the "why was this built this way?" amnesia: the why is written down,
next to the code, at the moment it was decided.

---

## 4. How a dev actually uses this — a walkthrough

You're implementing `002-user-auth`. Tasks are approved; you're on `T-004`.

**Normal flow — you tag as you go:**

```python
# REQ-003: lock the account after 5 consecutive failures
if failures >= 5:
    lock_account(user)
```
Commit: `feat(T-004): lock account after 5 failures [REQ-003]`. Record the SHA next to
T-004 in `tasks.md`, flip it to `done`. CI runs `trace.py` — REQ-003 now has code; it
also needs a test, which you wrote first (TDD), so the matrix is green.

**Drift appears — product says "make it 3 failures, and notify the user":**

1. You **stop**. Note it in `context.md` ("2026-06-12 — limit lowered to 3 + notify, per product").
2. `/specify --amend 002-user-auth` → edit REQ-003, add REQ-007 (notify), append the
   Changelog row, status → `needs-approval`.
3. You review and approve.
4. `/tasks --refresh 002-user-auth` → T-004 marked `stale`, a new task added for REQ-007.
5. `/implement` resumes from the stale/ new tasks. `trace.py` stays honest throughout —
   the moment REQ-003's code changes without a matching test, CI is red.

**Two weeks later, someone asks "why 3 and not 5?"** — the answer is one line in
`context.md` and one row in the spec Changelog. No archaeology.

---

## 5. The gate, too

Drift's cousin is starting to build before the design is agreed. `scripts/check_gate.py`
refuses to let `/implement` begin until `spec.md` and `plan.md` are `approved`:

```bash
python scripts/check_gate.py specs/002-user-auth
# ❌ plan.md is 'draft', must be 'approved' before implementing
# Gate CLOSED — get human approval first (Constitution, Article VII).
```

`/implement` runs this as its first step, so the gate isn't just a sentence in a doc.

---

## TL;DR

| Concern | Mechanism |
|---------|-----------|
| Spec quietly lies about the code | `scripts/trace.py` fails CI on uncovered/unknown REQs |
| "Did anything drift?" | `/sync` — the reverse path, three-state classification |
| Something changed mid-build | amendment protocol: `--amend` → `--refresh` → re-approve |
| "Why was it built this way?" | `context.md` decision journal, read on every resume |
| Building before design is agreed | `scripts/check_gate.py` blocks `/implement` |

Discipline asks people to remember. Mechanism makes the build remember for them.
