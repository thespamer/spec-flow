# Spec: Per-client API rate limiting

- **Feature ID:** 001-api-rate-limit
- **Status:** approved
- **Author:** Juliano Souza
- **Date:** 2026-06-08

## Summary
Protect the public API from abuse by limiting how many requests a single client
key may make per minute, returning a clear, standards-compliant response when the
limit is exceeded.

## Actors
- API client (identified by API key)
- API gateway / middleware

## Requirements (EARS)
| ID | Type | Requirement | Acceptance criteria |
|----|------|-------------|---------------------|
| REQ-001 | event-driven | When a client sends a request, the system shall count it against that client's rolling 60-second window. | A counter increments per key; window slides correctly across the minute boundary. |
| REQ-002 | unwanted | If a client exceeds 100 requests in the window, then the system shall reject further requests with HTTP 429. | The 101st request in a window returns 429. |
| REQ-003 | ubiquitous | The system shall include `Retry-After` and `X-RateLimit-Remaining` headers on every API response. | Both headers present with correct values on 200 and 429. |
| REQ-004 | state-driven | While a client is below its limit, the system shall pass the request through unchanged. | Requests 1–100 behave identically to the unlimited path. |

## Non-goals
- Per-endpoint or tiered limits (future feature).
- Distributed limiting across regions (single-node window is acceptable for v1).

## Open questions
- (resolved) Limit is fixed at 100/min for v1.

## Changelog
| Date | Change | Why | Trigger |
|------|--------|-----|---------|
| 2026-06-08 | initial spec | — | specify |
