"""
===============================================================================
Dummy Data Generator for Data Engineering Project
===============================================================================

Summary
-------
This script generates realistic dummy data for an e-commerce application.

It performs the following steps:

1. Connects to the database.
2. Deletes any existing tables and recreates them.
3. Generates random data for:
   - Customers
   - Products
   - Payments
   - Orders
   - Customer Feedback
   - Sentiment Analysis
4. Inserts all generated data into the database.
5. Returns the total number of records created for each table.

Why is this useful?
-------------------
Instead of manually entering data, this script creates thousands of realistic
records that can be used for:

- API development
- SQL practice
- ETL pipelines
- Data Engineering projects
- Machine Learning experiments
- Dashboard development
- Performance testing

This script is intended for development and testing environments only.
===============================================================================
"""

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

# -----------------------------------------------------------------------------
# Add the project root directory to Python's import path.
#
# This allows the script to import modules from the "app" package,
# even when this file is executed directly.
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# -----------------------------------------------------------------------------
# Import SQLAlchemy database objects.
#
# Base      -> Base class for all ORM models
# Session   -> Creates database sessions
# engine    -> Database connection
#
# Import all database models.
# -----------------------------------------------------------------------------
from app.db import Base, Session, engine
from app.db import Customer, Feedback, Order, Payment, Product, Sentiment


def generate_dummy_data(record_count: int = 1000) -> dict[str, int]:
    """
    Generate dummy data for all database tables.

    Parameters
    ----------
    record_count : int
        Number of records to generate for each entity.

    Returns
    -------
    dict
        Number of rows inserted into each table.
    """

    # -------------------------------------------------------------------------
    # Delete all existing database tables.
    #
    # This ensures every execution starts with a clean database.
    # -------------------------------------------------------------------------
    Base.metadata.drop_all(engine)

    # -------------------------------------------------------------------------
    # Recreate all tables using SQLAlchemy models.
    # -------------------------------------------------------------------------
    Base.metadata.create_all(engine)

    # -------------------------------------------------------------------------
    # If user requests zero or fewer records,
    # simply return empty counts.
    # -------------------------------------------------------------------------
    if record_count <= 0:
        return {
            "customers": 0,
            "products": 0,
            "orders": 0,
            "feedback": 0,
            "sentiments": 0,
        }

    # -------------------------------------------------------------------------
    # Fix the random seed.
    #
    # Using the same seed ensures the same random values are generated every
    # time, making testing repeatable.
    # -------------------------------------------------------------------------
    random.seed(42)

    # -------------------------------------------------------------------------
    # Lookup values used for generating realistic dummy data.
    # -------------------------------------------------------------------------
    countries = [
        "USA",
        "Canada",
        "UK",
        "Germany",
        "France",
        "India",
        "Japan",
        "Australia",
    ]

    categories = [
        "Electronics",
        "Home",
        "Fashion",
        "Books",
        "Sports",
        "Beauty",
    ]

    product_names = [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Tablet",
        "Smartwatch",
        "Camera",
        "Speaker",
        "Printer",
        "Keyboard",
        "Mouse",
    ]

    sentiment_labels = [
        "positive",
        "neutral",
        "negative",
    ]

    # -------------------------------------------------------------------------
    # Lists that temporarily store generated ORM objects.
    #
    # They are inserted into the database together later.
    # -------------------------------------------------------------------------
    customers = []
    products = []
    payments = []
    orders = []
    feedbacks = []
    sentiments = []

    # -------------------------------------------------------------------------
    # Generate all records.
    # -------------------------------------------------------------------------
    for idx in range(record_count):

        # ---------------------------------------------------------------------
        # Create Customer
        # ---------------------------------------------------------------------
        customer = Customer(
            customer_id=idx + 1,
            name=f"Customer {idx + 1}",
            email=f"customer{idx + 1}@example.com",
            country=random.choice(countries),
        )
        customers.append(customer)

        # ---------------------------------------------------------------------
        # Create Product
        # ---------------------------------------------------------------------
        product = Product(
            product_id=idx + 1,
            product_name=f"{random.choice(product_names)} {idx + 1}",
            category=random.choice(categories),
            price=round(random.uniform(10, 500), 2),
        )
        products.append(product)

        # ---------------------------------------------------------------------
        # Create Payment
        # ---------------------------------------------------------------------
        payment = Payment(
            payment_id=idx + 1,
            payment_method=random.choice(
                [
                    "card",
                    "cash",
                    "wallet",
                    "bank_transfer",
                ]
            ),
            amount=round(random.uniform(20, 600), 2),
            status=random.choice(
                [
                    "paid",
                    "pending",
                    "failed",
                ]
            ),
        )
        payments.append(payment)

        # ---------------------------------------------------------------------
        # Create Order
        #
        # Links Customer, Product and Payment together.
        # ---------------------------------------------------------------------
        order = Order(
            order_id=idx + 1,
            customer_id=customer.customer_id,
            product_id=product.product_id,
            payment_id=payment.payment_id,
            order_date=datetime.utcnow() - timedelta(
                days=random.randint(1, 365)
            ),
            quantity=random.randint(1, 5),
            total_amount=round(product.price * random.randint(1, 3), 2),
        )
        orders.append(order)

        # ---------------------------------------------------------------------
        # Select a random customer review.
        # ---------------------------------------------------------------------
        feedback_text = random.choice(
            [
                "Great product and excellent quality",
                "Good value for money",
                "Delivery was late",
                "Very satisfied with the experience",
                "Average product, could be better",
                "Fantastic support and fast shipping",
            ]
        )

        # ---------------------------------------------------------------------
        # Create Feedback
        # ---------------------------------------------------------------------
        feedback = Feedback(
            feedback_id=idx + 1,
            customer_id=customer.customer_id,
            product_id=product.product_id,
            rating=random.randint(1, 5),
            feedback_text=feedback_text,
            feedback_date=datetime.utcnow()
            - timedelta(days=random.randint(1, 180)),
        )
        feedbacks.append(feedback)

        # ---------------------------------------------------------------------
        # Create Sentiment Analysis Result
        #
        # Simulates an NLP model classifying customer feedback.
        # ---------------------------------------------------------------------
        sentiment = Sentiment(
            sentiment_id=idx + 1,
            feedback_id=feedback.feedback_id,
            sentiment=random.choice(sentiment_labels),
            confidence=round(random.uniform(0.5, 0.99), 2),
            model_name=random.choice(
                [
                    "bert-base",
                    "roberta-base",
                    "distilbert",
                ]
            ),
        )
        sentiments.append(sentiment)

    # -------------------------------------------------------------------------
    # Open a database session.
    # -------------------------------------------------------------------------
    with Session(engine) as session:

        # ---------------------------------------------------------------------
        # Remove existing records.
        #
        # Although the tables were recreated above, this guarantees the tables
        # are empty before inserting fresh data.
        # ---------------------------------------------------------------------
        session.query(Feedback).delete()
        session.query(Sentiment).delete()
        session.query(Order).delete()
        session.query(Payment).delete()
        session.query(Product).delete()
        session.query(Customer).delete()

        session.commit()

        # ---------------------------------------------------------------------
        # Insert all generated records in batches.
        #
        # add_all() is much faster than inserting one record at a time.
        # ---------------------------------------------------------------------
        session.add_all(customers)
        session.add_all(products)
        session.add_all(payments)
        session.add_all(orders)
        session.add_all(feedbacks)
        session.add_all(sentiments)

        # ---------------------------------------------------------------------
        # Save all changes permanently.
        # ---------------------------------------------------------------------
        session.commit()

    # -------------------------------------------------------------------------
    # Return a summary of inserted records.
    # -------------------------------------------------------------------------
    return {
        "customers": len(customers),
        "products": len(products),
        "orders": len(orders),
        "feedback": len(feedbacks),
        "sentiments": len(sentiments),
    }


# -----------------------------------------------------------------------------
# Script Entry Point
#
# This block runs only when the file is executed directly:
#
#     python generate_dummy_data.py
#
# It does NOT run when the function is imported into another module.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(generate_dummy_data(1000))