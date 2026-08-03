"""Pydantic schema for customer payloads."""

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    """Common customer fields shared by create and read schemas."""

    name: str
    email: EmailStr
    country: str


class CustomerCreate(CustomerBase):
    """Schema used when creating a new customer."""


class CustomerRead(CustomerBase):
    """Schema used when returning a customer."""

    customer_id: int
