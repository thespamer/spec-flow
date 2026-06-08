# Plan: Per-client API rate limiting  (001-api-rate-limit)

- **Status:** approved
- **Spec:** ./spec.md

## Approach
A middleware sits in front of the route handlers. It keys a sliding-window
counter by API key in an in-process store, decides allow/deny, and decorates the
response with rate-limit headers.

## Components
| Component | New/changed | Responsibility | Serves REQs |
|-----------|-------------|----------------|-------------|
| `RateLimiter` | new | sliding-window counting + allow/deny decision | REQ-001, REQ-002, REQ-004 |
| `rate_limit_middleware` | new | wire limiter into the request path, set headers | REQ-002, REQ-003 |
| store (in-memory) | new | per-key timestamps with TTL eviction | REQ-001 |

## Data flow
request → middleware → RateLimiter.check(key) → {allow → handler, deny → 429} →
middleware sets `Retry-After` / `X-RateLimit-Remaining` → response.

## Contracts / interfaces
- `RateLimiter.check(key: str, now: float) -> Decision(allowed: bool, remaining: int, retry_after: int)`

## Decisions (ADR-style)
### D1 — Sliding window over fixed window
- **Alternatives:** fixed window, token bucket
- **Chosen because:** avoids burst-at-boundary of fixed window; simpler than token
  bucket for a fixed per-minute cap (REQ-002).

## Risks & rollback
- In-memory store lost on restart → acceptable for v1 (single node, non-goal covers it).
- Rollback: feature-flag the middleware; disabling it restores the unlimited path.

## Test strategy
Unit tests for `RateLimiter` (window math, boundary), integration tests through the
middleware for 429 + headers.

## Requirement coverage
| REQ | Covered by component(s) |
|-----|-------------------------|
| REQ-001 | RateLimiter, store |
| REQ-002 | RateLimiter, middleware |
| REQ-003 | middleware |
| REQ-004 | RateLimiter |
