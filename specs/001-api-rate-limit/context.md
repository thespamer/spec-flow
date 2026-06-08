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

## Session resume
- **Last commit:** (not started)
- **Next task:** T-001
- **Watch out:** write the window-boundary test first — it's the easy thing to get wrong.
