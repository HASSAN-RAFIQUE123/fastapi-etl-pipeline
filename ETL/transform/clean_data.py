"""Data cleaning utilities for the ETL workflow."""


def clean_data(data: list[dict[str, object]]) -> list[dict[str, object]]:
    """Normalize the incoming rows by trimming string values."""
    cleaned: list[dict[str, object]] = []
    for row in data:
        cleaned_row = {}
        for key, value in row.items():
            if isinstance(value, str):
                cleaned_row[key] = value.strip()
            else:
                cleaned_row[key] = value
        cleaned.append(cleaned_row)
    return cleaned
