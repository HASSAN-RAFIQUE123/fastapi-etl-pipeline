"""Pydantic schema for product payloads."""

from pydantic import BaseModel


class ProductBase(BaseModel):
    """Common product fields shared by create and read schemas."""

    product_name: str
    category: str
    price: float


class ProductCreate(ProductBase):
    """Schema used when creating a new product."""


class ProductRead(ProductBase):
    """Schema used when returning a product."""

    product_id: int
