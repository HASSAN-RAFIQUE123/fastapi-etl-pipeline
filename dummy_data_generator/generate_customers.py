"""Dummy customer generation helpers."""


def generate_customers(count: int) -> list[dict[str, object]]:
    """Return a lightweight customer payload list for seeding."""
    return [{"customer_id": index, "name": f"Customer {index}"} for index in range(1, count + 1)]
