"""Service layer for payment-related business operations."""

from app.repositories.payment_repository import PaymentRepository


class PaymentService:
    """Coordinate payment workflow and repository access."""

    def __init__(self, repository: PaymentRepository | None = None) -> None:
        self.repository = repository or PaymentRepository()

    def get_all(self) -> list[dict[str, object]]:
        """Return all payments from the repository."""
        return self.repository.get_all()
