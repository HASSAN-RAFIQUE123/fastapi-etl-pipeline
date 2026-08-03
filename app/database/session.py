"""Database session helpers and engine initialization."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL, DB_ECHO

engine = create_engine(DATABASE_URL, future=True, echo=DB_ECHO)
SessionLocal = Session
