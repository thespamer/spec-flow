"""Integration tests for rate-limit middleware. REQ-002, REQ-003."""

from api_rate_limit.middleware import rate_limit_middleware

LIMIT = 100
WINDOW_SECONDS = 60


def _make_app():
    """Minimal handler that returns 200 with a body."""
    def handler(environ, start_response):
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"ok"]

    return handler


def test_req_002_rejects_101st_request_with_429():
    """REQ-002: the 101st request in a window returns HTTP 429."""
    app = rate_limit_middleware(_make_app(), limit=LIMIT, window_seconds=WINDOW_SECONDS)
    key = "client-a"
    status_headers: list[tuple[str, list[tuple[str, str]]]] = []

    def capture_start_response(status, headers, exc_info=None):
        status_headers.append((status, headers))
        return lambda data: None

    environ_base = {"HTTP_X_API_KEY": key, "REQUEST_METHOD": "GET"}

    # Same window instant so all 100 count together (sliding window, not spread over 100s).
    for _ in range(LIMIT):
        status_headers.clear()
        list(app({**environ_base, "rate_limit.now": "1000.0"}, capture_start_response))

    status_headers.clear()
    list(app({**environ_base, "rate_limit.now": "1000.0"}, capture_start_response))

    status, _ = status_headers[0]
    assert status.startswith("429")


def test_req_003_headers_on_success():
    """REQ-003: Retry-After and X-RateLimit-Remaining on 200 responses."""
    app = rate_limit_middleware(_make_app(), limit=LIMIT, window_seconds=WINDOW_SECONDS)
    captured: list[tuple[str, list[tuple[str, str]]]] = []

    def capture(status, headers, exc_info=None):
        captured.append((status, headers))
        return lambda data: None

    list(app(
        {"HTTP_X_API_KEY": "client-b", "REQUEST_METHOD": "GET", "rate_limit.now": "2000.0"},
        capture,
    ))

    status, headers = captured[0]
    header_map = {k.lower(): v for k, v in headers}

    assert status.startswith("200")
    assert "retry-after" in header_map
    assert "x-ratelimit-remaining" in header_map
    assert int(header_map["x-ratelimit-remaining"]) == LIMIT - 1


def test_req_003_headers_on_429():
    """REQ-003: Retry-After and X-RateLimit-Remaining on 429 responses."""
    app = rate_limit_middleware(_make_app(), limit=2, window_seconds=WINDOW_SECONDS)
    captured: list[tuple[str, list[tuple[str, str]]]] = []

    def capture(status, headers, exc_info=None):
        captured.append((status, headers))
        return lambda data: None

    environ = {"HTTP_X_API_KEY": "client-c", "REQUEST_METHOD": "GET", "rate_limit.now": "3000.0"}

    for _ in range(2):
        captured.clear()
        list(app(environ, capture))

    captured.clear()
    list(app(environ, capture))

    status, headers = captured[0]
    header_map = {k.lower(): v for k, v in headers}

    assert status.startswith("429")
    assert "retry-after" in header_map
    assert int(header_map["retry-after"]) >= 1
    assert "x-ratelimit-remaining" in header_map
    assert int(header_map["x-ratelimit-remaining"]) == 0
