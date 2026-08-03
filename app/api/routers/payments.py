"""Payment-related API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/")
def list_payments() -> dict[str, str]:
    """Return a simple placeholder response for the payment API."""
    return {"message": "payments endpoint"}
