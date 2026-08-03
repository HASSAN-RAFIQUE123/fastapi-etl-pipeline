"""Repository for product data access."""

from app.db import list_products


class ProductRepository:
    """Read product records using the existing database helpers."""

    def get_all(self) -> list[dict[str, object]]:
        """Return all product rows as JSON-ready dictionaries."""
        return list_products()
