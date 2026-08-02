import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test_app.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    import app.config as config_module
    import app.db as db_module
    import app.main as main_module

    importlib.reload(config_module)
    importlib.reload(db_module)
    importlib.reload(main_module)
    db_module.init_db()

    with TestClient(main_module.app) as test_client:
        yield test_client


def test_seed_and_list_business_data(client):
    response = client.post("/seed/dummy-data", json={"record_count": 1000})
    assert response.status_code == 200

    customers = client.get("/customers")
    assert customers.status_code == 200
    assert len(customers.json()) == 1000

    products = client.get("/products")
    assert products.status_code == 200
    assert len(products.json()) == 1000

    feedback = client.get("/feedback")
    assert feedback.status_code == 200
    assert len(feedback.json()) == 1000

    analytics = client.get("/analytics/feedback-summary")
    assert analytics.status_code == 200
    payload = analytics.json()
    assert payload["total_feedback"] == 1000


def test_get_feedback_by_date_range(client):
    from datetime import datetime

    import app.db as db_module

    with db_module.Session(db_module.engine) as session:
        session.add_all(
            [
                db_module.Feedback(
                    feedback_id=10001,
                    customer_id=1,
                    product_id=1,
                    rating=5,
                    feedback_text="Excellent",
                    feedback_date=datetime(2026, 1, 10),
                ),
                db_module.Feedback(
                    feedback_id=10002,
                    customer_id=2,
                    product_id=2,
                    rating=4,
                    feedback_text="Great",
                    feedback_date=datetime(2026, 3, 20),
                ),
                db_module.Feedback(
                    feedback_id=10003,
                    customer_id=3,
                    product_id=3,
                    rating=2,
                    feedback_text="Late delivery",
                    feedback_date=datetime(2026, 4, 5),
                ),
            ]
        )
        session.commit()

    response = client.get(
        "/feedback/date-range",
        params={"start_date": "2026-01-01", "end_date": "2026-03-31"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert {item["feedback_id"] for item in payload} == {10001, 10002}
