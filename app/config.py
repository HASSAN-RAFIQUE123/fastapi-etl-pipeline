"""
===============================================================================
Application Configuration Settings
===============================================================================

Summary
-------
This module is responsible for managing the application's configuration.

Instead of hardcoding values throughout the project, all important settings
(such as the database connection, application name, and debug options) are
stored in one central location.

The configuration values are loaded from:

1. Environment Variables
2. .env File (if available)
3. Default values (fallback)

Why is this important?
----------------------
Keeping configuration separate from the application code makes the project:

✔ Easier to maintain
✔ More secure
✔ Environment independent
✔ Production ready

Typical environments include:

Development
------------
DATABASE_URL = sqlite:///./app.db

Testing
--------
DATABASE_URL = sqlite:///:memory:

Production
-----------
DATABASE_URL = postgresql://username:password@host:5432/database

Benefits
--------
Instead of changing source code for every environment,
only the environment variables need to change.

This follows the Twelve-Factor App methodology, which is widely used in
modern cloud applications.
===============================================================================
"""

# -----------------------------------------------------------------------------
# Import the built-in os module.
#
# The os module allows Python to interact with the operating system.
#
# In this file it is mainly used to read environment variables.
# -----------------------------------------------------------------------------
import os

# -----------------------------------------------------------------------------
# Import load_dotenv from python-dotenv.
#
# This package loads variables from a .env file into the system environment,
# making them accessible through os.getenv().
#
# Example:
#
# DATABASE_URL=postgresql://localhost/mydb
# APP_NAME=Customer API
# -----------------------------------------------------------------------------
from dotenv import load_dotenv


# -----------------------------------------------------------------------------
# Load environment variables from a .env file.
#
# If a .env file exists in the project root, all variables inside it become
# available through os.getenv().
#
# If no .env file exists, this function simply does nothing.
#
# Example .env
#
# DATABASE_URL=postgresql://localhost:5432/customerdb
# APP_NAME=Customer API
# -----------------------------------------------------------------------------
load_dotenv()


# -----------------------------------------------------------------------------
# Database Connection String
#
# os.getenv() checks whether DATABASE_URL exists as an environment variable.
#
# If it exists:
#
#     Use that value.
#
# Otherwise:
#
#     Use SQLite as the default database.
#
# This allows the application to run immediately without additional setup.
#
# Development:
#     sqlite:///./app.db
#
# Production:
#     postgresql://username:password@host/database
# -----------------------------------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db",
)


# -----------------------------------------------------------------------------
# Application Name
#
# This value is displayed in:
#
# - Swagger UI
# - OpenAPI Documentation
# - FastAPI title
#
# It can also be used in logs and monitoring tools.
#
# If APP_NAME is not defined in the environment,
# the default name will be:
#
# "API Generator and API ETL"
# -----------------------------------------------------------------------------
APP_NAME = os.getenv(
    "APP_NAME",
    "API Generator and API ETL",
)


# -----------------------------------------------------------------------------
# SQLAlchemy SQL Logging
#
# DB_ECHO determines whether SQLAlchemy prints every SQL query executed.
#
# Environment Variable:
#
# DB_ECHO=True
#
# Accepted True Values:
#
# 1
# true
# yes
# on
#
# Everything else becomes False.
#
# Examples:
#
# DB_ECHO=1
# DB_ECHO=true
# DB_ECHO=yes
# DB_ECHO=on
#
# When enabled, SQLAlchemy displays SQL statements such as:
#
# SELECT * FROM customers;
#
# INSERT INTO products ...
#
# This is extremely useful during development and debugging.
#
# It is usually disabled in production because:
#
# - It slows the application slightly.
# - It can expose sensitive information in logs.
# -----------------------------------------------------------------------------
DB_ECHO = os.getenv(
    "DB_ECHO",
    "0",
).lower() in {
    "1",
    "true",
    "yes",
    "on",
}