"""Pydantic schema for feedback payloads."""

from datetime import datetime

from pydantic import BaseModel


class FeedbackBase(BaseModel):
    """Common feedback fields shared by create and read schemas."""

    customer_id: int
    product_id: int
    rating: int
    feedback_text: str
    feedback_date: datetime


class FeedbackCreate(FeedbackBase):
    """Schema used when creating a new feedback entry."""


class FeedbackRead(FeedbackBase):
    """Schema used when returning feedback."""

    feedback_id: int
