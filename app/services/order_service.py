"""Service layer for order-related business operations."""

from app.repositories.order_repository import OrderRepository


class OrderService:
    """Coordinate order workflow and repository access."""

    def __init__(self, repository: OrderRepository | None = None) -> None:
        self.repository = repository or OrderRepository()

    def get_all(self) -> list[dict[str, object]]:
        """Return all orders from the repository."""
        return self.repository.get_all()
