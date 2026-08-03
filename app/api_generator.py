"""
===============================================================================
FastAPI Route & ETL Project Explorer
===============================================================================

Summary
-------
This utility script helps developers quickly understand the current state of
the project without manually browsing multiple files.

The script performs three main tasks:

1. Displays all registered FastAPI API routes.
2. Shows available ETL notebooks and output folders.
3. Prints a step-by-step guide for adding a new API endpoint.

Why this script exists
----------------------
In large projects, developers often need a quick overview of:

- Which APIs already exist
- Which ETL notebooks are available
- Where ETL output files are stored
- How to add a new endpoint

Instead of searching through the entire project, this script summarizes the
important information in one place.

Typical Usage
-------------
Run the script from the project root:

    python explore_project.py

Expected Output
---------------
Current API routes:
    GET /customers
    GET /orders
    POST /sync

ETL Assets:
    Notebook: ETL/customer_etl.ipynb
    Folder: ETL/output

API Creation Guide:
    Step-by-step instructions for creating a new endpoint.

This script is intended as a developer productivity tool and does not modify
any application data.
===============================================================================
"""

# -----------------------------------------------------------------------------
# Import future annotations.
#
# This allows type hints to be evaluated lazily (as strings), improving
# compatibility and reducing some circular import issues.
# -----------------------------------------------------------------------------
from __future__ import annotations

# -----------------------------------------------------------------------------
# Import Path for working with files and folders in a platform-independent way.
#
# pathlib is preferred over os.path because it provides a cleaner and more
# object-oriented interface.
# -----------------------------------------------------------------------------
from pathlib import Path


# -----------------------------------------------------------------------------
# Function: show_existing_routes()
#
# Purpose:
#   Display all API routes currently registered in the FastAPI application.
#
# This is useful for developers who want to quickly inspect available endpoints.
# -----------------------------------------------------------------------------
def show_existing_routes() -> None:
    """Print the current FastAPI routes from the application."""

    # -------------------------------------------------------------------------
    # Try importing the FastAPI app instance.
    #
    # If the application cannot be imported (missing dependency, syntax error,
    # incorrect path, etc.), display the error instead of crashing.
    # -------------------------------------------------------------------------
    try:
        from app.main import app

    except Exception as exc:  # pragma: no cover - defensive

        # ---------------------------------------------------------------------
        # Display a helpful error message.
        # ---------------------------------------------------------------------
        print(f"Unable to import the app: {exc}")
        return

    # -------------------------------------------------------------------------
    # Print heading.
    # -------------------------------------------------------------------------
    print("Current API routes:")

    # -------------------------------------------------------------------------
    # FastAPI stores every registered endpoint inside app.routes.
    #
    # Iterate through each route and display:
    #   - HTTP methods (GET, POST, PUT, etc.)
    #   - URL path
    # -------------------------------------------------------------------------
    for route in app.routes:

        # Get the endpoint URL.
        path = getattr(route, "path", None)

        # Get allowed HTTP methods.
        methods = sorted(getattr(route, "methods", set()) or set())

        # Display only valid routes.
        if path and methods:
            print(f"- {'|'.join(methods)} {path}")


# -----------------------------------------------------------------------------
# Function: show_etl_context()
#
# Purpose:
#   Display ETL notebooks and generated output folders.
#
# This helps developers understand which ETL jobs already exist.
# -----------------------------------------------------------------------------
def show_etl_context() -> None:
    """Print the ETL notebooks and output folders available in the project."""

    # -------------------------------------------------------------------------
    # Define the ETL root directory.
    # -------------------------------------------------------------------------
    etl_root = Path("ETL")

    # -------------------------------------------------------------------------
    # Search for every Jupyter Notebook (*.ipynb)
    # -------------------------------------------------------------------------
    notebooks = sorted(
        p.name
        for p in etl_root.glob("*.ipynb")
    )

    # -------------------------------------------------------------------------
    # Search for every subfolder except Jupyter checkpoint folders.
    # -------------------------------------------------------------------------
    output_folders = sorted(
        p.name
        for p in etl_root.iterdir()
        if p.is_dir() and p.name != ".ipynb_checkpoints"
    )

    print("\nETL assets:")

    # -------------------------------------------------------------------------
    # Display notebook list.
    # -------------------------------------------------------------------------
    if notebooks:

        for notebook in notebooks:
            print(f"- Notebook: {etl_root / notebook}")

    else:
        print("- No notebooks found in ETL/")

    # -------------------------------------------------------------------------
    # Display output folders.
    # -------------------------------------------------------------------------
    if output_folders:

        for folder in output_folders:
            print(f"- Folder: {etl_root / folder}")

    else:
        print("- No ETL output folders found")


# -----------------------------------------------------------------------------
# Function: show_new_api_template()
#
# Purpose:
#   Display a simple guide explaining how to create a new API endpoint.
#
# This serves as documentation for new developers.
# -----------------------------------------------------------------------------
def show_new_api_template() -> None:
    """Print a reusable example for creating a new endpoint."""

    print("\nHow to create a new API endpoint:")

    # -------------------------------------------------------------------------
    # Step 1
    #
    # Create the database helper function.
    # -------------------------------------------------------------------------
    print("1. Add a database helper in app/db.py")
    print("   Example: def get_customer_orders(customer_id): ...")

    # -------------------------------------------------------------------------
    # Step 2
    #
    # Register the endpoint inside FastAPI.
    # -------------------------------------------------------------------------
    print("2. Expose it in app/main.py")
    print("   Example:")

    print("   @app.get('/customers/{customer_id}/orders')")

    print("   def get_customer_orders(customer_id: int):")

    print("       return list_customer_orders(customer_id)")

    # -------------------------------------------------------------------------
    # Step 3
    #
    # Start the FastAPI server and test the endpoint.
    # -------------------------------------------------------------------------
    print("3. Start the server and test it")

    print("   uvicorn app.main:app --reload")

    print("   curl http://127.0.0.1:8000/customers/1/orders")


# -----------------------------------------------------------------------------
# Script Entry Point
#
# This block executes only when this file is run directly.
#
# Example:
#
#     python explore_project.py
#
# It does NOT execute when this module is imported elsewhere.
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Display all registered API routes.
    show_existing_routes()

    # Display ETL notebooks and folders.
    show_etl_context()

    # Display API creation guide.
    show_new_api_template()