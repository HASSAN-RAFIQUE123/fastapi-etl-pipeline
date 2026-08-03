"""Pagination helpers for list endpoints."""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    """Simple pagination container for API responses."""

    items: list[T]
    page: int
    page_size: int
    total: int
