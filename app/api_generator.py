"""Helper script for exploring the FastAPI routes and ETL assets.

This file makes the project surface easier to understand. It prints the routes that are
currently registered in the app, shows a small template for adding a new endpoint, and
summarizes the ETL notebooks and output folders that live inside the ETL directory.
"""

from __future__ import annotations

from pathlib import Path


def show_existing_routes() -> None:
    """Print the current FastAPI routes from the app instance."""
    try:
        from app.main import app
    except Exception as exc:  # pragma: no cover - defensive
        print(f"Unable to import the app: {exc}")
        return

    print("Current API routes:")
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = sorted(getattr(route, "methods", set()) or set())
        if path and methods:
            print(f"- {'|'.join(methods)} {path}")


def show_etl_context() -> None:
    """Print the ETL notebooks and output folders available in the project."""
    etl_root = Path("ETL")
    notebooks = sorted(p.name for p in etl_root.glob("*.ipynb"))
    output_folders = sorted(
        p.name for p in etl_root.iterdir() if p.is_dir() and p.name != ".ipynb_checkpoints"
    )

    print("\nETL assets:")
    if notebooks:
        for notebook in notebooks:
            print(f"- Notebook: {etl_root / notebook}")
    else:
        print("- No notebooks found in ETL/")

    if output_folders:
        for folder in output_folders:
            print(f"- Folder: {etl_root / folder}")
    else:
        print("- No ETL output folders found")


def show_new_api_template() -> None:
    """Print a reusable example for creating a new endpoint."""
    print("\nHow to create a new API endpoint:")
    print("1. Add a database helper in app/db.py")
    print("   Example: def get_customer_orders(customer_id): ...")
    print("2. Expose it in app/main.py")
    print("   Example:")
    print("   @app.get('/customers/{customer_id}/orders')")
    print("   def get_customer_orders(customer_id: int):")
    print("       return list_customer_orders(customer_id)")
    print("3. Start the server and test it")
    print("   uvicorn app.main:app --reload")
    print("   curl http://127.0.0.1:8000/customers/1/orders")


if __name__ == "__main__":
    show_existing_routes()
    show_etl_context()
    show_new_api_template()
