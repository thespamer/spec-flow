"""Sliding-window rate limiter. REQ-001, REQ-002, REQ-004."""

from __future__ import annotations

from dataclasses import dataclass

from api_rate_limit.store import InMemoryStore


@dataclass(frozen=True)
class Decision:
    allowed: bool
    remaining: int
    retry_after: int


class RateLimiter:
    """REQ-001, REQ-004: sliding-window allow/deny with per-key counters."""

    def __init__(
        self,
        limit: int = 100,
        window_seconds: float = 60.0,
        store: InMemoryStore | None = None,
    ) -> None:
        self._limit = limit
        self._window_seconds = window_seconds
        self._store = store or InMemoryStore()

    def check(self, key: str, now: float) -> Decision:
        """REQ-001: count against rolling window; REQ-004: allow when below limit."""
        entries = self._store.prune(key, now, self._window_seconds)

        if len(entries) >= self._limit:
            # REQ-002: oldest entry determines when a slot frees up.
            retry_after = max(1, int(entries[0] + self._window_seconds - now) + 1)
            return Decision(allowed=False, remaining=0, retry_after=retry_after)

        count_before = len(entries)
        self._store.record(key, now)
        remaining = self._limit - count_before - 1
        return Decision(allowed=True, remaining=remaining, retry_after=0)
