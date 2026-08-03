"""Small helpers shared by the application."""

from typing import Any


def to_serializable(value: Any) -> Any:
    """Convert values to JSON-safe forms when possible."""
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value
