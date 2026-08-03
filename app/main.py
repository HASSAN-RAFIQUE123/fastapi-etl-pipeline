"""
=========================================================
FastAPI Main Application

Summary:
- Creates the FastAPI application.
- Initializes the database.
- Defines all API endpoints.
- Returns HTML and JSON responses.
- Connects the API with the database helper functions.
=========================================================
"""

# Import FastAPI classes.
from fastapi import FastAPI, HTTPException

# Import HTML response support.
from fastapi.responses import HTMLResponse

# Import request validation models.
from pydantic import BaseModel, Field
"""
=============================================================================
FastAPI Application Entry Point

Summary:
- Creates the FastAPI application.
- Initializes the database at startup.
- Defines all REST API endpoints.
- Receives HTTP requests.
- Calls database helper functions.
- Returns HTML or JSON responses.
=============================================================================
"""

# Import FastAPI framework and HTTP exception handling.
from fastapi import FastAPI, HTTPException

# Import HTML response class.
from fastapi.responses import HTMLResponse

# Import Pydantic models for request validation.
from pydantic import BaseModel, Field

# Import application configuration.
from .config import APP_NAME

# Import all required database helper functions.
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

# Create the FastAPI application.
app = FastAPI(title=APP_NAME)


# Request model for executing SQL queries.
class QueryRequest(BaseModel):
    """Request payload used for ad-hoc SQL queries."""

    # SQL query provided by the user.
    sql: str


# Request model for generating dummy data.
class SeedRequest(BaseModel):
    """Request payload used when creating dummy records."""

    # Number of records to generate (minimum 1).
    record_count: int = Field(default=1000, ge=1)


# Run automatically when the application starts.
@app.on_event("startup")
def startup_event() -> None:
    """Initialize the database tables as soon as the app starts."""

    # Create database tables if they don't exist.
    init_db()


# Home page endpoint.
@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    """Serve the dashboard HTML page."""

    # Open the HTML file.
    with open("templates/index.html", "r", encoding="utf-8") as handle:

        # Return HTML content.
        return handle.read()


# Health check endpoint.
@app.get("/health")
def health_check() -> dict[str, str]:
    """Return an OK payload when the API and database are reachable."""

    try:

        # Test database connection.
        test_connection()

        # Return success response.
        return {"status": "ok"}

    except Exception as exc:

        # Return HTTP 500 if an error occurs.
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# List all database tables.
@app.get("/tables")
def list_tables() -> dict[str, list[str]]:
    """Return the names of the tables available in the connected database."""

    # Fetch table names.
    return {"tables": get_tables()}


# Execute a raw SQL query.
@app.post("/query")
def execute_query(payload: QueryRequest) -> dict[str, object]:
    """Execute a raw SQL query and return the result as JSON."""

    # Import SQL text function.
    from sqlalchemy import text

    # Import database engine.
    from .db import engine

    try:

        # Open database connection.
        with engine.connect() as conn:

            # Execute SQL query.
            result = conn.execute(text(payload.sql))

            # Fetch all returned rows.
            rows = result.fetchall()

            # Get column names.
            columns = list(result.keys())

            # Return columns and rows as JSON.
            return {
                "columns": columns,
                "rows": [dict(zip(columns, row)) for row in rows],
            }

    except Exception as exc:

        # Return HTTP 400 for invalid SQL.
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    # Generate dummy data and store it in the database.
@app.post("/seed/dummy-data")
def seed_dummy_data_endpoint(payload: SeedRequest) -> dict[str, object]:
    """Seed the database with the requested number of dummy records."""

    # Generate the requested number of dummy records.
    return seed_dummy_data(payload.record_count)


# Get all customers.
@app.get("/customers")
def get_customers() -> list[dict[str, object]]:
    """Return all customers stored in the database."""

    # Retrieve all customer records.
    return list_customers()


# Get all products.
@app.get("/products")
def get_products() -> list[dict[str, object]]:
    """Return all products stored in the database."""

    # Retrieve all product records.
    return list_products()


# Get all orders.
@app.get("/orders")
def get_orders() -> list[dict[str, object]]:
    """Return all orders stored in the database."""

    # Retrieve all order records.
    return list_orders()


# Get all customer feedback.
@app.get("/feedback")
def get_feedback() -> list[dict[str, object]]:
    """Return all feedback records stored in the database."""

    # Retrieve all feedback records.
    return list_feedback()


# Get feedback between two dates.
#
# Example:
# /feedback/date-range?start_date=2025-01-01&end_date=2025-12-31
@app.get("/feedback/date-range")
def get_feedback_by_date_range(start_date: str, end_date: str) -> list[dict[str, object]]:
    """Return feedback records whose dates fall between the provided start and end dates."""

    # Retrieve feedback within the specified date range.
    return list_feedback_by_date_range(start_date, end_date)


# Get all sentiment analysis results.
@app.get("/sentiments")
def get_sentiments() -> list[dict[str, object]]:
    """Return all sentiment analysis records stored in the database."""

    # Retrieve all sentiment records.
    return list_sentiments()


# Get feedback analytics summary.
@app.get("/analytics/feedback-summary")
def get_feedback_summary() -> dict[str, object]:
    """Return a compact feedback analytics summary."""

    # Return calculated analytics such as average rating,
    # positive reviews, and negative reviews.
    return feedback_summary()