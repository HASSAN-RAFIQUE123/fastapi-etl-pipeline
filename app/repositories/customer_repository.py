"""Repository for customer data access."""

from app.db import list_customers


class CustomerRepository:
    """Read customer records using the existing database helpers."""

    def get_all(self) -> list[dict[str, object]]:
        """Return all customer rows as JSON-ready dictionaries."""
        return list_customers()
