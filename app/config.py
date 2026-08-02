"""Application configuration settings.

This module centralizes the environment-based configuration used by the FastAPI app and
SQLAlchemy. It loads values from the local environment or falls back to sensible defaults
so the project can run without extra setup.
"""

import os

from dotenv import load_dotenv

# Load any values from a local .env file when present.
load_dotenv()

# Default database connection string for local development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Human-readable application name used by FastAPI docs and the UI.
APP_NAME = os.getenv("APP_NAME", "API Generator and API ETL")

# Toggle SQLAlchemy SQL echoing for debugging purposes.
DB_ECHO = os.getenv("DB_ECHO", "0").lower() in {"1", "true", "yes", "on"}
