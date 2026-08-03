"""
===============================================================================
Database Models & Database Helper Functions
===============================================================================

Summary
-------
This module is the heart of the application's database layer.

It performs the following responsibilities:

1. Creates the SQLAlchemy database engine.
2. Defines all ORM (Object Relational Mapping) models.
3. Creates database tables.
4. Tests database connectivity.
5. Retrieves table information.
6. Seeds the database with dummy data.
7. Provides helper functions for querying data.
8. Computes analytics summaries.

This module acts as the bridge between FastAPI and the database.

Application
        │
        ▼
Database Helper Functions
        │
        ▼
SQLAlchemy ORM
        │
        ▼
SQLite / PostgreSQL
"""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Import the sys module.
#
# Used to modify Python's import path dynamically so the project modules
# can be imported regardless of the current working directory.
# -----------------------------------------------------------------------------
import sys

# -----------------------------------------------------------------------------
# Import datetime utilities.
#
# datetime
#     Represents dates and times.
#
# Used by Order and Feedback tables.
# -----------------------------------------------------------------------------
from datetime import datetime

# -----------------------------------------------------------------------------
# pathlib.Path provides an object-oriented way to work with file paths.
#
# It is preferred over os.path because it is cleaner and cross-platform.
# -----------------------------------------------------------------------------
from pathlib import Path
# -----------------------------------------------------------------------------
# Import SQLAlchemy core components.
#
# create_engine
#     Creates the connection between Python and the database.
#
# func
#     Provides SQL aggregate functions like:
#         AVG()
#         COUNT()
#         MAX()
#         MIN()
#
# text
#     Allows execution of raw SQL queries.
# -----------------------------------------------------------------------------
from sqlalchemy import create_engine, func, text

# -----------------------------------------------------------------------------
# Import SQLAlchemy ORM components.
#
# Mapped
#     Used for type-safe ORM model attributes (SQLAlchemy 2.x style).
#
# Session
#     Represents a database session.
#     A session is used to:
#         - Insert data
#         - Update data
#         - Delete data
#         - Query data
#
# declarative_base()
#     Creates the parent class from which all ORM models inherit.
#
# mapped_column()
#     Defines a database column.
# -----------------------------------------------------------------------------
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column

# -----------------------------------------------------------------------------
# Determine the project's root directory.
#
# __file__
#     Current Python file.
#
# resolve()
#     Returns the absolute path.
#
# parents[1]
#     Goes one directory above the current folder.
#
# Example:
#
# app/
#     db.py
#
# becomes
#
# project/
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# -----------------------------------------------------------------------------
# Ensure the project root exists in Python's module search path.
#
# This allows imports such as:
#
# from app.config import DATABASE_URL
#
# to work regardless of where the script is executed.
# -----------------------------------------------------------------------------
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -----------------------------------------------------------------------------
# Import application configuration.
#
# DATABASE_URL
#     Database connection string.
#
# DB_ECHO
#     Controls whether SQLAlchemy prints generated SQL statements.
# -----------------------------------------------------------------------------
from .config import DATABASE_URL, DB_ECHO

# -----------------------------------------------------------------------------
# Create the SQLAlchemy Engine.
#
# The engine manages:
#
#     Python
#         │
#         ▼
# SQLAlchemy Engine
#         │
#         ▼
# SQLite / PostgreSQL
#
# future=True
#     Enables SQLAlchemy 2.x behavior.
#
# echo=DB_ECHO
#     Prints SQL queries if debugging is enabled.
# -----------------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=DB_ECHO,
)

# -----------------------------------------------------------------------------
# Create the Declarative Base.
#
# Every ORM model in this project inherits from Base.
#
# Example:
#
# class Customer(Base):
#
# SQLAlchemy uses this Base object to know which models belong
# to the database schema.
# -----------------------------------------------------------------------------
Base = declarative_base()

# -----------------------------------------------------------------------------
# Alias for SQLAlchemy Session.
#
# Instead of writing:
#
# Session(engine)
#
# throughout the project, we keep a common name.
#
# In larger projects this is usually created using sessionmaker(),
# but this alias works for this learning project.
# -----------------------------------------------------------------------------
SessionLocal = Session


# =============================================================================
# CUSTOMER MODEL
# =============================================================================
#
# Represents one customer in the database.
#
# SQL Table:
#
# customers
#
# Example
#
# customer_id | name       | email              | country
# ----------------------------------------------------------
# 1           | John Smith | john@gmail.com     | Germany
#
# Every row in the customers table becomes one Customer object.
# =============================================================================
class Customer(Base):
    """Represents a customer record in the database."""

    # -------------------------------------------------------------------------
    # Name of the SQL table.
    # -------------------------------------------------------------------------
    __tablename__ = "customers"

    # -------------------------------------------------------------------------
    # Primary Key.
    #
    # Every customer has a unique ID.
    # -------------------------------------------------------------------------
    customer_id: Mapped[int] = mapped_column(primary_key=True)

    # Customer full name.
    name: Mapped[str]

    # Customer email address.
    email: Mapped[str]

    # Customer country.
    country: Mapped[str]

    # -------------------------------------------------------------------------
    # Convert ORM object into a Python dictionary.
    #
    # FastAPI can easily serialize dictionaries into JSON responses.
    # -------------------------------------------------------------------------
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "country": self.country,
        }


# =============================================================================
# PRODUCT MODEL
# =============================================================================
#
# Represents products sold by the company.
#
# SQL Table:
#
# products
#
# product_id | product_name | category | price
# ---------------------------------------------
# 1          | Laptop       | Tech     | 1200
#
# One row in SQL = One Product object.
# =============================================================================
class Product(Base):
    """Represents a product record in the database."""

    # SQL table name.
    __tablename__ = "products"

    # Primary key.
    product_id: Mapped[int] = mapped_column(primary_key=True)

    # Product name.
    product_name: Mapped[str]

    # Product category.
    category: Mapped[str]

    # Product selling price.
    price: Mapped[float]

    # Convert ORM object into dictionary.
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "category": self.category,
            "price": self.price,
        }
    # =============================================================================
# PAYMENT MODEL
# =============================================================================
#
# Represents a customer's payment information.
#
# SQL Table:
#
# payments
#
# payment_id | payment_method | amount | status
# ------------------------------------------------
# 1          | card           | 299.99 | paid
#
# Every payment made by a customer is stored here.
#
# In a production application this table may also contain:
#
# - Transaction ID
# - Payment Gateway
# - Currency
# - Payment Timestamp
# - Refund Status
# - Invoice Number
# =============================================================================
class Payment(Base):
    """Represents a payment record in the database."""

    # -------------------------------------------------------------------------
    # SQL table name.
    # -------------------------------------------------------------------------
    __tablename__ = "payments"

    # -------------------------------------------------------------------------
    # Primary Key
    #
    # Every payment has a unique identifier.
    # -------------------------------------------------------------------------
    payment_id: Mapped[int] = mapped_column(primary_key=True)

    # Payment type used by customer.
    payment_method: Mapped[str]

    # Total payment amount.
    amount: Mapped[float]

    # Current payment status.
    #
    # Example:
    # Paid
    # Pending
    # Failed
    status: Mapped[str]

    # -------------------------------------------------------------------------
    # Convert ORM object into dictionary.
    #
    # FastAPI converts this dictionary into JSON.
    # -------------------------------------------------------------------------
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "payment_id": self.payment_id,
            "payment_method": self.payment_method,
            "amount": self.amount,
            "status": self.status,
        }


# =============================================================================
# ORDER MODEL
# =============================================================================
#
# Represents a customer's order.
#
# This table connects:
#
# Customer
# Product
# Payment
#
# Therefore it acts as the central transaction table.
#
# Example
#
# customer -----> order <------ product
#                    |
#                    |
#                 payment
#
# In a production database these IDs should be Foreign Keys.
#
# Example:
#
# customer_id -> customers.customer_id
# product_id -> products.product_id
# payment_id -> payments.payment_id
#
# This guarantees referential integrity.
# =============================================================================
class Order(Base):
    """Represents a purchase order record in the database."""

    # SQL table name.
    __tablename__ = "orders"

    # Primary key.
    order_id: Mapped[int] = mapped_column(primary_key=True)

    # Customer who placed the order.
    #
    # Production:
    #
    # ForeignKey("customers.customer_id")
    customer_id: Mapped[int] = mapped_column()

    # Purchased product.
    #
    # Production:
    #
    # ForeignKey("products.product_id")
    product_id: Mapped[int] = mapped_column()

    # Payment used.
    #
    # Production:
    #
    # ForeignKey("payments.payment_id")
    payment_id: Mapped[int] = mapped_column()

    # Date and time when order was created.
    order_date: Mapped[datetime]

    # Number of purchased items.
    quantity: Mapped[int]

    # Total order value.
    total_amount: Mapped[float]

    # Convert ORM object into dictionary.
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "payment_id": self.payment_id,
            "order_date": self.order_date.isoformat(),
            "quantity": self.quantity,
            "total_amount": self.total_amount,
        }


# =============================================================================
# FEEDBACK MODEL
# =============================================================================
#
# Stores customer reviews after purchasing products.
#
# Example
#
# Customer
#     │
#     ▼
# Feedback
#     │
#     ▼
# Product
#
# Example Record
#
# Rating:
# 5
#
# Review:
# Excellent product.
#
# Date:
# 2026-08-01
#
# This table is later used for analytics and sentiment analysis.
# =============================================================================
class Feedback(Base):
    """Represents a feedback submission from a customer."""

    # SQL table name.
    __tablename__ = "feedback"

    # Primary key.
    feedback_id: Mapped[int] = mapped_column(primary_key=True)

    # Customer who submitted the review.
    customer_id: Mapped[int] = mapped_column()

    # Reviewed product.
    product_id: Mapped[int] = mapped_column()

    # Customer rating.
    #
    # Usually:
    #
    # 1–5 Stars
    rating: Mapped[int]

    # Written customer review.
    feedback_text: Mapped[str]

    # Date when review was submitted.
    feedback_date: Mapped[datetime]

    # Convert ORM object into dictionary.
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "feedback_id": self.feedback_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "rating": self.rating,
            "feedback_text": self.feedback_text,
            "feedback_date": self.feedback_date.isoformat(),
        }


# =============================================================================
# SENTIMENT MODEL
# =============================================================================
#
# Stores AI/NLP sentiment analysis results.
#
# Example
#
# Feedback
#     │
#     ▼
# Sentiment Analysis
#
# Positive
# Neutral
# Negative
#
# Confidence:
#
# 0.97
#
# Model:
#
# bert-base
#
# This table simulates Machine Learning output.
# =============================================================================
class Sentiment(Base):
    """Represents a sentiment analysis result for a feedback record."""

    # SQL table name.
    __tablename__ = "sentiments"

    # Primary key.
    sentiment_id: Mapped[int] = mapped_column(primary_key=True)

    # Related feedback record.
    #
    # Production:
    #
    # ForeignKey("feedback.feedback_id")
    feedback_id: Mapped[int] = mapped_column()

    # Predicted sentiment.
    #
    # Positive
    # Neutral
    # Negative
    sentiment: Mapped[str]

    # Confidence score returned by ML model.
    #
    # Example:
    #
    # 0.98
    confidence: Mapped[float]

    # Name of AI model.
    #
    # Example:
    #
    # bert-base
    # roberta-base
    model_name: Mapped[str]

    # Convert ORM object into dictionary.
    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""

        return {
            "sentiment_id": self.sentiment_id,
            "feedback_id": self.feedback_id,
            "sentiment": self.sentiment,
            "confidence": self.confidence,
            "model_name": self.model_name,
        }
customer_id = mapped_column(ForeignKey("customers.customer_id"))
product_id = mapped_column(ForeignKey("products.product_id"))
payment_id = mapped_column(ForeignKey("payments.payment_id"))
feedback_id = mapped_column(ForeignKey("feedback.feedback_id"))
