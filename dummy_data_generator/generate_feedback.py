"""Dummy feedback generation helpers."""


def generate_feedback(count: int) -> list[dict[str, object]]:
    """Return a lightweight feedback payload list for seeding."""
    return [{"feedback_id": index, "rating": 5, "feedback_text": f"Feedback {index}"} for index in range(1, count + 1)]
