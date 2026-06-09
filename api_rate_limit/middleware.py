"""WSGI rate-limit middleware. REQ-002, REQ-003."""

from __future__ import annotations

import time
from typing import Callable

from api_rate_limit.rate_limiter import RateLimiter

_WSGIApp = Callable[..., object]
_StartResponse = Callable[..., object]


def _api_key(environ: dict) -> str:
    return environ.get("HTTP_X_API_KEY", "")


def _now(environ: dict) -> float:
    raw = environ.get("rate_limit.now")
    if raw is not None:
        return float(raw)
    return time.time()


def rate_limit_middleware(
    app: _WSGIApp,
    limit: int = 100,
    window_seconds: float = 60.0,
    limiter: RateLimiter | None = None,
) -> _WSGIApp:
    """REQ-002, REQ-003: enforce limits and decorate every response with headers."""
    _limiter = limiter or RateLimiter(limit=limit, window_seconds=window_seconds)

    def middleware(environ: dict, start_response: _StartResponse):
        key = _api_key(environ)
        decision = _limiter.check(key, _now(environ))

        def start_with_headers(status: str, headers: list, exc_info=None):
            # REQ-003: rate-limit headers on every response.
            extra = [
                ("X-RateLimit-Remaining", str(decision.remaining)),
                ("Retry-After", str(decision.retry_after)),
            ]
            return start_response(status, headers + extra, exc_info)

        if not decision.allowed:
            # REQ-002: reject over-limit requests with HTTP 429.
            start_with_headers(
                "429 Too Many Requests",
                [("Content-Type", "text/plain")],
            )
            return [b"rate limit exceeded"]

        return app(environ, start_with_headers)

    return middleware
