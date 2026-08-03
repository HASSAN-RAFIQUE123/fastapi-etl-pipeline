"""Entry point for the ETL pipeline orchestration.

This module is a placeholder for the more advanced ETL workflow described in the
requested folder structure. It keeps the project organized while pointing to the
extract, transform, and load phases.
"""

from etl.extract.extract_customers import extract_customers
from etl.transform.clean_data import clean_data
from etl.load.load_database import load_database


def run_pipeline() -> None:
    """Run the ETL pipeline in three phases."""
    data = extract_customers()
    cleaned = clean_data(data)
    load_database(cleaned)
