"""Metadata helpers for ETL runs."""

from dataclasses import dataclass


@dataclass
class ETLMetadata:
    """Describe the inputs and outputs used by an ETL run."""

    source: str
    destination: str
    records_loaded: int
