"""Order-related API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
def list_orders() -> dict[str, str]:
    """Return a simple placeholder response for the order API."""
    return {"message": "orders endpoint"}
