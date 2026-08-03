"""Service layer for feedback-related business operations."""

from app.repositories.feedback_repository import FeedbackRepository


class FeedbackService:
    """Coordinate feedback workflow and repository access."""

    def __init__(self, repository: FeedbackRepository | None = None) -> None:
        self.repository = repository or FeedbackRepository()

    def get_all(self) -> list[dict[str, object]]:
        """Return all feedback entries from the repository."""
        return self.repository.get_all()
