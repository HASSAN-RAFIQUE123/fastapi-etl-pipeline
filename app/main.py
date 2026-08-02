"""FastAPI application entry point.

This module defines the API surface for the sample data platform. It exposes routes for
health checks, database inspection, dummy-data seeding, and reading business data from the
SQLite-backed database.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .config import APP_NAME
from .db import (
    feedback_summary,
    get_tables,
    init_db,
    list_customers,
    list_feedback,
    list_feedback_by_date_range,
    list_orders,
    list_products,
    list_sentiments,
    seed_dummy_data,
    test_connection,
)

# Create the FastAPI app instance with the configured title.
app = FastAPI(title=APP_NAME)


class QueryRequest(BaseModel):
    """Request payload used for ad-hoc SQL queries."""

    sql: str


class SeedRequest(BaseModel):
    """Request payload used when creating dummy records."""

    record_count: int = Field(default=1000, ge=1)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize the database tables as soon as the app starts."""
    init_db()


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    """Serve the dashboard HTML page."""
    with open("templates/index.html", "r", encoding="utf-8") as handle:
        return handle.read()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return an OK payload when the API and database are reachable."""
    try:
        test_connection()
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/tables")
def list_tables() -> dict[str, list[str]]:
    """Return the names of the tables available in the connected database."""
    return {"tables": get_tables()}


@app.post("/query")
def execute_query(payload: QueryRequest) -> dict[str, object]:
    """Execute a raw SQL query and return the result as JSON."""
    from sqlalchemy import text

    from .db import engine

    try:
        with engine.connect() as conn:
            result = conn.execute(text(payload.sql))
            rows = result.fetchall()
            columns = list(result.keys())
            return {"columns": columns, "rows": [dict(zip(columns, row)) for row in rows]}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/seed/dummy-data")
def seed_dummy_data_endpoint(payload: SeedRequest) -> dict[str, object]:
    """Seed the database with the requested number of dummy records."""
    return seed_dummy_data(payload.record_count)


@app.get("/customers")
def get_customers() -> list[dict[str, object]]:
    """Return all customers stored in the database."""
    return list_customers()


@app.get("/products")
def get_products() -> list[dict[str, object]]:
    """Return all products stored in the database."""
    return list_products()


@app.get("/orders")
def get_orders() -> list[dict[str, object]]:
    """Return all orders stored in the database."""
    return list_orders()


@app.get("/feedback")
def get_feedback() -> list[dict[str, object]]:
    """Return all feedback records stored in the database."""
    return list_feedback()


@app.get("/feedback/date-range")
def get_feedback_by_date_range(start_date: str, end_date: str) -> list[dict[str, object]]:
    """Return feedback records whose dates fall between the provided start and end dates."""
    return list_feedback_by_date_range(start_date, end_date)


@app.get("/sentiments")
def get_sentiments() -> list[dict[str, object]]:
    """Return all sentiment analysis records stored in the database."""
    return list_sentiments()


@app.get("/analytics/feedback-summary")
def get_feedback_summary() -> dict[str, object]:
    """Return a compact feedback analytics summary."""
    return feedback_summary()
