"""Unit tests for sliding-window rate limiting. REQ-001, REQ-004."""

from api_rate_limit.rate_limiter import RateLimiter

WINDOW_SECONDS = 60
LIMIT = 100


def test_req_001_counts_requests_per_key_in_window():
    """REQ-001: counter increments per key within the rolling window."""
    limiter = RateLimiter(limit=LIMIT, window_seconds=WINDOW_SECONDS)
    key = "client-a"

    d1 = limiter.check(key, now=1000.0)
    d2 = limiter.check(key, now=1001.0)

    assert d1.allowed is True
    assert d2.allowed is True
    assert d1.remaining == LIMIT - 1
    assert d2.remaining == LIMIT - 2


def test_req_001_window_slides_across_minute_boundary():
    """REQ-001: requests older than 60s fall out of the window."""
    limiter = RateLimiter(limit=LIMIT, window_seconds=WINDOW_SECONDS)
    key = "client-a"

    for i in range(LIMIT):
        limiter.check(key, now=0.0 + i * 0.1)

    # All timestamps are < 60s old at t=59.9 — still at limit.
    at_edge = limiter.check(key, now=59.9)
    assert at_edge.allowed is False

    # At t=61.0 the earliest requests (t=0..0.9) have slid out; room again.
    after_slide = limiter.check(key, now=61.0)
    assert after_slide.allowed is True


def test_req_001_keys_are_independent():
    """REQ-001: each API key maintains its own counter."""
    limiter = RateLimiter(limit=2, window_seconds=WINDOW_SECONDS)

    limiter.check("alice", now=10.0)
    limiter.check("alice", now=11.0)
    alice_blocked = limiter.check("alice", now=12.0)

    bob_ok = limiter.check("bob", now=12.0)

    assert alice_blocked.allowed is False
    assert bob_ok.allowed is True


def test_req_004_allows_requests_below_limit():
    """REQ-004: requests 1–100 are allowed."""
    limiter = RateLimiter(limit=LIMIT, window_seconds=WINDOW_SECONDS)
    key = "client-a"

    for i in range(LIMIT):
        decision = limiter.check(key, now=1000.0 + i)
        assert decision.allowed is True, f"request {i + 1} should be allowed"


def test_req_004_remaining_reflects_headroom():
    """REQ-004: remaining count tracks unused quota on the happy path."""
    limiter = RateLimiter(limit=LIMIT, window_seconds=WINDOW_SECONDS)
    key = "client-a"

    d = limiter.check(key, now=500.0)
    assert d.allowed is True
    assert d.remaining == LIMIT - 1
