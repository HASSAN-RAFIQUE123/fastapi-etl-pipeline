"""Database models and helper functions.

This module defines the SQLAlchemy models for the sample business data and provides the
helper functions used by the FastAPI routes and ETL workflow. It is the bridge between the
application layer and the SQLite database.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import Mapped, Session, declarative_base, mapped_column

# Ensure the project root is importable when this file is executed from different locations.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .config import DATABASE_URL, DB_ECHO

# Create the SQLAlchemy engine that connects to the configured database.
engine = create_engine(DATABASE_URL, future=True, echo=DB_ECHO)

# Declarative base for all ORM models.
Base = declarative_base()

# Alias used throughout the project for database sessions.
SessionLocal = Session


class Customer(Base):
    """Represents a customer record in the database."""

    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    country: Mapped[str]

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "country": self.country,
        }


class Product(Base):
    """Represents a product record in the database."""

    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    category: Mapped[str]
    price: Mapped[float]

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "category": self.category,
            "price": self.price,
        }


class Payment(Base):
    """Represents a payment record in the database."""

    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(primary_key=True)
    payment_method: Mapped[str]
    amount: Mapped[float]
    status: Mapped[str]

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""
        return {
            "payment_id": self.payment_id,
            "payment_method": self.payment_method,
            "amount": self.amount,
            "status": self.status,
        }


class Order(Base):
    """Represents a purchase order record in the database."""

    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    payment_id: Mapped[int] = mapped_column()
    order_date: Mapped[datetime]
    quantity: Mapped[int]
    total_amount: Mapped[float]

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


class Feedback(Base):
    """Represents a feedback submission from a customer."""

    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    rating: Mapped[int]
    feedback_text: Mapped[str]
    feedback_date: Mapped[datetime]

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


class Sentiment(Base):
    """Represents a sentiment analysis result for a feedback record."""

    __tablename__ = "sentiments"

    sentiment_id: Mapped[int] = mapped_column(primary_key=True)
    feedback_id: Mapped[int] = mapped_column()
    sentiment: Mapped[str]
    confidence: Mapped[float]
    model_name: Mapped[str]

    def to_dict(self) -> dict[str, object]:
        """Return a serializable dictionary for API responses."""
        return {
            "sentiment_id": self.sentiment_id,
            "feedback_id": self.feedback_id,
            "sentiment": self.sentiment,
            "confidence": self.confidence,
            "model_name": self.model_name,
        }


def init_db() -> None:
    """Create all tables if they do not already exist."""
    Base.metadata.create_all(engine)


def test_connection() -> None:
    """Perform a lightweight database check to ensure the connection works."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def get_tables() -> list[str]:
    """Return the list of tables available in the connected database."""
    dialect = engine.dialect.name

    if dialect == "sqlite":
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    elif dialect == "postgresql":
        query = (
            "SELECT tablename FROM pg_catalog.pg_tables "
            "WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'"
        )
    elif dialect == "mysql":
        query = "SHOW TABLES"
    else:
        raise NotImplementedError(f"Table listing is not supported for dialect: {dialect}")

    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [row[0] for row in result.fetchall()]


def seed_dummy_data(record_count: int = 1000) -> dict[str, int]:
    """Seed the database with dummy rows using the generator module."""
    init_db()

    from dummy_data_generator.generate_dummy_data import generate_dummy_data

    return generate_dummy_data(record_count)


def list_customers(limit: int | None = None) -> list[dict[str, object]]:
    """Return all customers in order, optionally limiting the number of rows."""
    with Session(engine) as session:
        query = session.query(Customer).order_by(Customer.customer_id)
        if limit is not None:
            query = query.limit(limit)
        rows = query.all()
        return [row.to_dict() for row in rows]


def list_products(limit: int | None = None) -> list[dict[str, object]]:
    """Return all products in order, optionally limiting the number of rows."""
    with Session(engine) as session:
        query = session.query(Product).order_by(Product.product_id)
        if limit is not None:
            query = query.limit(limit)
        rows = query.all()
        return [row.to_dict() for row in rows]


def list_orders(limit: int | None = None) -> list[dict[str, object]]:
    """Return all orders in order, optionally limiting the number of rows."""
    with Session(engine) as session:
        query = session.query(Order).order_by(Order.order_id)
        if limit is not None:
            query = query.limit(limit)
        rows = query.all()
        return [row.to_dict() for row in rows]


def list_feedback(limit: int | None = None) -> list[dict[str, object]]:
    """Return all feedback entries in order, optionally limiting the number of rows."""
    with Session(engine) as session:
        query = session.query(Feedback).order_by(Feedback.feedback_id)
        if limit is not None:
            query = query.limit(limit)
        rows = query.all()
        return [row.to_dict() for row in rows]


def list_feedback_by_date_range(start_date: str, end_date: str) -> list[dict[str, object]]:
    """Return feedback entries whose feedback_date falls within the provided date range."""
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    with Session(engine) as session:
        rows = (
            session.query(Feedback)
            .filter(Feedback.feedback_date >= start_dt)
            .filter(Feedback.feedback_date <= end_dt)
            .order_by(Feedback.feedback_id)
            .all()
        )
        return [row.to_dict() for row in rows]


def list_sentiments(limit: int | None = None) -> list[dict[str, object]]:
    """Return all sentiment records in order, optionally limiting the number of rows."""
    with Session(engine) as session:
        query = session.query(Sentiment).order_by(Sentiment.sentiment_id)
        if limit is not None:
            query = query.limit(limit)
        rows = query.all()
        return [row.to_dict() for row in rows]


def feedback_summary() -> dict[str, object]:
    """Compute a simple analytics summary for feedback data."""
    with Session(engine) as session:
        total_feedback = session.query(Feedback).count()
        positive = session.query(Feedback).filter(Feedback.rating >= 4).count()
        negative = session.query(Feedback).filter(Feedback.rating <= 2).count()
        average_rating = session.query(func.avg(Feedback.rating)).scalar()
        return {
            "total_feedback": total_feedback,
            "positive_reviews": positive,
            "negative_reviews": negative,
            "average_rating": round(float(average_rating), 2) if average_rating is not None else 0,
        }
