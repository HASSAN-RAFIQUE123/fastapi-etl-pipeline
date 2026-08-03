"""Application-wide exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Register a simple handler for unexpected errors."""

    @app.exception_handler(Exception)
    async def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        """Return a consistent JSON error payload for unexpected failures."""
        return JSONResponse(status_code=500, content={"detail": str(exc)})
