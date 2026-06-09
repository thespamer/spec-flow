# Tasks: Per-client API rate limiting  (001-api-rate-limit)

- **Status:** approved
- **Plan:** ./plan.md

> Status legend: todo · doing · done · blocked · stale

| ID | Task | Serves | Component | depends_on | Tests | Status | Commit |
|----|------|--------|-----------|------------|-------|--------|--------|
| T-001 | Write failing unit tests for sliding-window math incl. boundary | REQ-001, REQ-004 | RateLimiter | — | test_rate_limiter.py | done | 51c0357 |
| T-002 | Implement RateLimiter + in-memory store to pass T-001 | REQ-001, REQ-004 | RateLimiter, store | T-001 | test_rate_limiter.py | done | e8cf5c3 |
| T-003 | Write failing integration tests for 429 + headers | REQ-002, REQ-003 | middleware | T-002 | test_middleware.py | done | 5f31fc2 |
| T-004 | Implement rate_limit_middleware to pass T-003 | REQ-002, REQ-003 | middleware | T-003 | test_middleware.py | done | pending |
| T-005 | Verify: traceability matrix + full suite green | all | — | T-004 | full suite | todo | — |

## Notes / blockers
- none yet
