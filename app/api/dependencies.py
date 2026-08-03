"""Shared dependencies used by the API routers.

These helpers keep the application layer thin while centralizing cross-cutting concerns
such as database session access and request validation.
"""

from typing import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for request-scoped operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
