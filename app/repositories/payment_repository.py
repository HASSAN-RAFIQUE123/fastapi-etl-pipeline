"""Repository for payment data access."""

from app.db import list_orders


class PaymentRepository:
    """Read payment records using the existing database helpers."""

    def get_all(self) -> list[dict[str, object]]:
        """Return all payment rows as JSON-ready dictionaries."""
        return list_orders()
