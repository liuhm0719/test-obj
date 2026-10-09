import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import RATE_LIMIT_PER_MINUTE


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._counters: dict[str, tuple[int, int]] = {}

    async def dispatch(self, request: Request, call_next):
        ip = (
            request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            if request.client is None
            else request.client.host
        )

        now = int(time.time())
        window_start = now // 60 * 60

        count, stored_window = self._counters.get(ip, (0, window_start))
        if stored_window != window_start:
            count = 0
            stored_window = window_start

        count += 1
        self._counters[ip] = (count, stored_window)

        if count > RATE_LIMIT_PER_MINUTE:
            retry_after = stored_window + 60 - int(time.time())
            return JSONResponse(
                status_code=429,
                headers={"Retry-After": str(retry_after)},
                content={"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"},
            )

        return await call_next(request)
