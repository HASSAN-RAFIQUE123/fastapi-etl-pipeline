"""Dummy product generation helpers."""


def generate_products(count: int) -> list[dict[str, object]]:
    """Return a lightweight product payload list for seeding."""
    return [{"product_id": index, "product_name": f"Product {index}", "price": float(index)} for index in range(1, count + 1)]
