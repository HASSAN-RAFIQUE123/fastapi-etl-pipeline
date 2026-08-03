"""Feedback-related API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/")
def list_feedback() -> dict[str, str]:
    """Return a simple placeholder response for the feedback API."""
    return {"message": "feedback endpoint"}
