# Context journal: Per-client API rate limiting  (001-api-rate-limit)

> Durable memory for this feature (Constitution, Article X). Update it as you work.

## Constraints
- v1 runs on a single node; no shared store across regions (see spec Non-goals).
- Must not add latency to the happy path beyond a single in-memory lookup.

## Assumptions
- 100 req/min is the right default for v1 (confirmed with product; revisit at GA).
- Clients are uniquely identified by API key; anonymous traffic is out of scope.

## Decisions log
| Date | Decision | Why | Trigger |
|------|----------|-----|---------|
| 2026-06-08 | Sliding window over fixed window | Avoids burst-at-boundary; simpler than token bucket for a fixed cap | plan |
| 2026-06-08 | In-memory store, no persistence | Single-node v1; restart-loss is acceptable per Non-goals | plan |

## Rejected alternatives
- Token bucket — rejected: more moving parts than needed for a fixed per-minute cap.
- Redis-backed counter — rejected for v1: pulls in infra a single node doesn't need yet.

## Open questions
- Should limits become per-tier later? Tracked as a future feature, not this one.

## Drift / sync log
| Date | State | Finding | Reconciliation |
|------|-------|---------|----------------|
| 2026-06-09 | spec ahead | REQ-001–004 declared & task-covered; no code, tests, or task commits yet | No amend needed. Proceed with `/implement` starting T-001. |
| 2026-06-09 | in sync | No unknown `REQ` markers in project code; no code-ahead drift | — |
| 2026-06-09 | in sync | `tasks.md` ↔ git: all T-001–T-005 are `todo`; no orphan commits | — |

## Session resume
- **Last commit:** 8dabb4a (T-004)
- **Next task:** T-005 (`/verify`)
- **Watch out:** T-003 101st-request test uses same `now` instant — spreading timestamps over 100s lets the sliding window evict early entries.

## Decisions log (continued)
| Date | Decision | Why | Trigger |
|------|----------|-----|---------|
| 2026-06-09 | `api_rate_limit/` package at repo root | Example feature ships in spec-flow repo itself; no pre-existing app layout | implement |
| 2026-06-09 | WSGI middleware + `rate_limit.now` test hook | Stdlib-only; injectable clock for deterministic integration tests | implement T-004 |
