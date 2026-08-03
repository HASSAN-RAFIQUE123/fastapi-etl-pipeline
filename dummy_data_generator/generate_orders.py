"""Dummy order generation helpers."""


def generate_orders(count: int) -> list[dict[str, object]]:
    """Return a lightweight order payload list for seeding."""
    return [{"order_id": index, "customer_id": index, "product_id": index} for index in range(1, count + 1)]
