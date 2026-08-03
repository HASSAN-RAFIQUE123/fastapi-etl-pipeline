"""Pydantic schema for payment payloads."""

from pydantic import BaseModel


class PaymentBase(BaseModel):
    """Common payment fields shared by create and read schemas."""

    payment_method: str
    amount: float
    status: str


class PaymentCreate(PaymentBase):
    """Schema used when creating a new payment."""


class PaymentRead(PaymentBase):
    """Schema used when returning a payment."""

    payment_id: int
