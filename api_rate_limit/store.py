"""In-memory per-key timestamp store. REQ-001."""

from __future__ import annotations


class InMemoryStore:
    """Per-key request timestamps with sliding-window eviction."""

    def __init__(self) -> None:
        self._timestamps: dict[str, list[float]] = {}

    def prune(self, key: str, now: float, window_seconds: float) -> list[float]:
        """REQ-001: drop timestamps outside the rolling window."""
        cutoff = now - window_seconds
        entries = self._timestamps.setdefault(key, [])
        self._timestamps[key] = [t for t in entries if t > cutoff]
        return self._timestamps[key]

    def record(self, key: str, now: float) -> None:
        """REQ-001: record a request timestamp for the key."""
        self._timestamps.setdefault(key, []).append(now)
