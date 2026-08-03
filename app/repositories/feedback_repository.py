"""Repository for feedback data access."""

from app.db import list_feedback


class FeedbackRepository:
    """Read feedback records using the existing database helpers."""

    def get_all(self) -> list[dict[str, object]]:
        """Return all feedback rows as JSON-ready dictionaries."""
        return list_feedback()
