import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.db import Base, Session, engine
from app.db import Customer, Feedback, Order, Payment, Product, Sentiment


def generate_dummy_data(record_count: int = 1000) -> dict[str, int]:
    """Create dummy customer, product, order, payment, feedback, and sentiment data.

    This function is meant to be easy to read and understand. It builds one record
    at a time, stores everything in memory, then inserts it into the database in one
    transaction for better performance.
    """

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    if record_count <= 0:
        return {"customers": 0, "products": 0, "orders": 0, "feedback": 0, "sentiments": 0}

    random.seed(42)

    countries = ["USA", "Canada", "UK", "Germany", "France", "India", "Japan", "Australia"]
    categories = ["Electronics", "Home", "Fashion", "Books", "Sports", "Beauty"]
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
    sentiment_labels = ["positive", "neutral", "negative"]

    customers = []
    products = []
    payments = []
    orders = []
    feedbacks = []
    sentiments = []

    for idx in range(record_count):
        customer = Customer(
            customer_id=idx + 1,
            name=f"Customer {idx + 1}",
            email=f"customer{idx + 1}@example.com",
            country=random.choice(countries),
        )
        customers.append(customer)

        product = Product(
            product_id=idx + 1,
            product_name=f"{random.choice(product_names)} {idx + 1}",
            category=random.choice(categories),
            price=round(random.uniform(10, 500), 2),
        )
        products.append(product)

        payment = Payment(
            payment_id=idx + 1,
            payment_method=random.choice(["card", "cash", "wallet", "bank_transfer"]),
            amount=round(random.uniform(20, 600), 2),
            status=random.choice(["paid", "pending", "failed"]),
        )
        payments.append(payment)

        order = Order(
            order_id=idx + 1,
            customer_id=customer.customer_id,
            product_id=product.product_id,
            payment_id=payment.payment_id,
            order_date=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            quantity=random.randint(1, 5),
            total_amount=round(product.price * random.randint(1, 3), 2),
        )
        orders.append(order)

        feedback_text = random.choice([
            "Great product and excellent quality",
            "Good value for money",
            "Delivery was late",
            "Very satisfied with the experience",
            "Average product, could be better",
            "Fantastic support and fast shipping",
        ])
        feedback = Feedback(
            feedback_id=idx + 1,
            customer_id=customer.customer_id,
            product_id=product.product_id,
            rating=random.randint(1, 5),
            feedback_text=feedback_text,
            feedback_date=datetime.utcnow() - timedelta(days=random.randint(1, 180)),
        )
        feedbacks.append(feedback)

        sentiment = Sentiment(
            sentiment_id=idx + 1,
            feedback_id=feedback.feedback_id,
            sentiment=random.choice(sentiment_labels),
            confidence=round(random.uniform(0.5, 0.99), 2),
            model_name=random.choice(["bert-base", "roberta-base", "distilbert"]),
        )
        sentiments.append(sentiment)

    with Session(engine) as session:
        session.query(Feedback).delete()
        session.query(Sentiment).delete()
        session.query(Order).delete()
        session.query(Payment).delete()
        session.query(Product).delete()
        session.query(Customer).delete()
        session.commit()

        session.add_all(customers)
        session.add_all(products)
        session.add_all(payments)
        session.add_all(orders)
        session.add_all(feedbacks)
        session.add_all(sentiments)
        session.commit()

    return {
        "customers": len(customers),
        "products": len(products),
        "orders": len(orders),
        "feedback": len(feedbacks),
        "sentiments": len(sentiments),
    }


if __name__ == "__main__":
    print(generate_dummy_data(1000))
