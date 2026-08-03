"""Service layer for customer-related business operations."""

from app.repositories.customer_repository import CustomerRepository


class CustomerService:
    """Coordinate customer workflow and repository access."""

    def __init__(self, repository: CustomerRepository | None = None) -> None:
        self.repository = repository or CustomerRepository()

    def get_all(self) -> list[dict[str, object]]:
        """Return all customers from the repository."""
        return self.repository.get_all()
