"""Core configuration helpers for the application."""

from app.config import APP_NAME, DATABASE_URL, DB_ECHO

# Re-export the environment-driven settings to keep the new package layout aligned.
APP_NAME = APP_NAME
DATABASE_URL = DATABASE_URL
DB_ECHO = DB_ECHO
