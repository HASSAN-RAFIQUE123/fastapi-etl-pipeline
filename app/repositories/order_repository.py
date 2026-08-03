"""Repository for order data access."""

from app.db import list_orders


class OrderRepository:
    """Read order records using the existing database helpers."""

    def get_all(self) -> list[dict[str, object]]:
        """Return all order rows as JSON-ready dictionaries."""
        return list_orders()
