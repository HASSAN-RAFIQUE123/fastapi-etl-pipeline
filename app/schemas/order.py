"""Pydantic schema for order payloads."""

from datetime import datetime

from pydantic import BaseModel


class OrderBase(BaseModel):
    """Common order fields shared by create and read schemas."""

    customer_id: int
    product_id: int
    payment_id: int
    order_date: datetime
    quantity: int
    total_amount: float


class OrderCreate(OrderBase):
    """Schema used when creating a new order."""


class OrderRead(OrderBase):
    """Schema used when returning an order."""

    order_id: int
