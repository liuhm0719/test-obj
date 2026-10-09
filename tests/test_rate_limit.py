import time
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

import app.middleware.rate_limit as rl_module
from app.main import app


def _find_rate_limit_middleware():
    """Walk the live middleware stack (requires app already started) to find the instance."""
    node = app.middleware_stack
    while node is not None:
        if isinstance(node, rl_module.RateLimitMiddleware):
            return node
        node = getattr(node, "app", None)
    raise RuntimeError("RateLimitMiddleware not found in middleware stack")


@pytest.fixture
def client_and_middleware():
    """Start the app, locate the middleware instance, clear counters, yield both."""
    original_limit = rl_module.RATE_LIMIT_PER_MINUTE
    with TestClient(app) as client:
        middleware = _find_rate_limit_middleware()
        middleware._counters.clear()
        yield client, middleware
        middleware._counters.clear()
    rl_module.RATE_LIMIT_PER_MINUTE = original_limit


def test_requests_within_limit(client_and_middleware):
    """All requests up to the limit should return 200."""
    client, _ = client_and_middleware
    limit = 5
    rl_module.RATE_LIMIT_PER_MINUTE = limit

    for _ in range(limit):
        response = client.get("/health")
        assert response.status_code == 200


def test_request_exceeding_limit_returns_429(client_and_middleware):
    """The request after the limit is hit must return 429 with expected body and header."""
    client, _ = client_and_middleware
    limit = 5
    rl_module.RATE_LIMIT_PER_MINUTE = limit

    for _ in range(limit):
        r = client.get("/health")
        assert r.status_code == 200

    response = client.get("/health")

    assert response.status_code == 429

    body = response.json()
    assert body.get("code") == "RATE_LIMIT_EXCEEDED"
    assert "message" in body

    retry_after = response.headers.get("Retry-After")
    assert retry_after is not None
    assert int(retry_after) > 0


def test_different_ips_counted_independently(client_and_middleware):
    """Two IPs each at their own counter should not interfere with each other."""
    client, middleware = client_and_middleware
    limit = 3
    rl_module.RATE_LIMIT_PER_MINUTE = limit

    window_start = int(time.time()) // 60 * 60

    # Saturate the IP TestClient uses ("testclient") — next request will be blocked.
    middleware._counters["testclient"] = (limit, window_start)
    # Give an independent IP a low count.
    middleware._counters["10.0.0.2"] = (1, window_start)

    # The next "testclient" request should be over the limit → 429.
    resp_over = client.get("/health")
    assert resp_over.status_code == 429

    # "10.0.0.2" counter must be unchanged — it was not the requester.
    assert middleware._counters["10.0.0.2"][0] == 1


def test_window_reset_allows_requests_again():
    """After the 60-second window expires, the counter resets and requests succeed."""
    limit = 3
    # Choose a base_time aligned to a window boundary so arithmetic is clean.
    base_time = 3660.0  # 3660 // 60 * 60 == 3660

    with patch("app.middleware.rate_limit.time") as mock_time:
        mock_time.time.return_value = base_time

        with TestClient(app) as client:
            middleware = _find_rate_limit_middleware()
            middleware._counters.clear()
            rl_module.RATE_LIMIT_PER_MINUTE = limit

            # Exhaust the limit.
            for _ in range(limit):
                r = client.get("/health")
                assert r.status_code == 200

            # Next request is blocked.
            r = client.get("/health")
            assert r.status_code == 429

            # Advance 61 seconds → new 60-second window bucket.
            mock_time.time.return_value = base_time + 61

            # Requests should be allowed again.
            r = client.get("/health")
            assert r.status_code == 200

