"""Dummy payment generation helpers."""


def generate_payments(count: int) -> list[dict[str, object]]:
    """Return a lightweight payment payload list for seeding."""
    return [{"payment_id": index, "amount": float(index), "status": "paid"} for index in range(1, count + 1)]
