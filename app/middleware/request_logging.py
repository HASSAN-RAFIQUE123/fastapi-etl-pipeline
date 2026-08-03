"""Middleware that logs incoming requests."""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log request metadata for observability and debugging."""

    async def dispatch(self, request: Request, call_next):
        """Log the path and method before handing off to the next layer."""
        print(f"{request.method} {request.url.path}")
        return await call_next(request)
