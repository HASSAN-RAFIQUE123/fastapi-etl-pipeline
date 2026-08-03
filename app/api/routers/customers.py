"""Customer-related API routes.

This module is intentionally lightweight and acts as a placeholder for the future
customer endpoints in the layered architecture.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
def list_customers() -> dict[str, str]:
    """Return a simple placeholder response for the customer API."""
    return {"message": "customers endpoint"}
