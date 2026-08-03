"""Product-related API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def list_products() -> dict[str, str]:
    """Return a simple placeholder response for the product API."""
    return {"message": "products endpoint"}
