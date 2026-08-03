"""Validation helpers for the application."""

from datetime import datetime


def is_valid_date(value: str) -> bool:
    """Return True when the provided string can be parsed as a date."""
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False
