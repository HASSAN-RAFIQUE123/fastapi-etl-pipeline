"""Service layer for product-related business operations."""

from app.repositories.product_repository import ProductRepository


class ProductService:
    """Coordinate product workflow and repository access."""

    def __init__(self, repository: ProductRepository | None = None) -> None:
        self.repository = repository or ProductRepository()

    def get_all(self) -> list[dict[str, object]]:
        """Return all products from the repository."""
        return self.repository.get_all()
