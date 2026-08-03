"""Seed the local database with dummy records.

This module is a simple entry point for the new dummy-data-generator structure so the
project can gradually move from the old single-file seeding approach to the new layout.
"""

from dummy_data_generator.generate_customers import generate_customers
from dummy_data_generator.generate_feedback import generate_feedback
from dummy_data_generator.generate_orders import generate_orders
from dummy_data_generator.generate_payments import generate_payments
from dummy_data_generator.generate_products import generate_products


def seed_database(count: int = 100) -> dict[str, list[dict[str, object]]]:
    """Generate sample records for each domain and return them as a dictionary."""
    return {
        "customers": generate_customers(count),
        "products": generate_products(count),
        "orders": generate_orders(count),
        "payments": generate_payments(count),
        "feedback": generate_feedback(count),
    }
