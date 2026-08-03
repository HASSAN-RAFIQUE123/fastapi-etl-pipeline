"""Seed the database with dummy data from the command line."""

from app.db import seed_dummy_data


if __name__ == "__main__":
    count = 1000
    result = seed_dummy_data(count)
    print(f"Seeded {result.get('customers', 0)} customers")
