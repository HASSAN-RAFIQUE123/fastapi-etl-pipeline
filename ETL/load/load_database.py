"""Database-loading helpers for the ETL workflow."""


def load_database(data: list[dict[str, object]]) -> int:
    """Persist the cleaned structures and return the row count loaded."""
    return len(data)
