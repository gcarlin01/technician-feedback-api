import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)

    from sqlalchemy.orm import sessionmaker

    TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)

    def override_get_db():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_feedback_can_be_created_listed_and_updated(client):
    create_response = client.post(
        "/api/v1/feedback",
        json={
            "technician_name": "Taylor",
            "feedback_text": "The app will not load my jobs.",
            "score": 1,
            "mood": "frustrated",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    feedback_id = created["id"]
    assert created["priority"] == "normal"
    assert created["status"] == "new"

    list_response = client.get("/api/v1/feedback")
    assert [item["id"] for item in list_response.json()] == [feedback_id]

    update_response = client.put(
        f"/api/v1/feedback/{feedback_id}",
        json={
            "technician_name": "Taylor",
            "feedback_text": "The app will not load my jobs.",
            "score": 1,
            "mood": "frustrated",
            "assigned_team": "Mobile",
            "priority": "high",
            "status": "in_progress",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["assigned_team"] == "Mobile"
    assert update_response.json()["priority"] == "high"
    assert update_response.json()["status"] == "in_progress"


def test_missing_feedback_returns_404(client):
    response = client.get("/api/v1/feedback/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Feedback not found"


def test_invalid_score_is_rejected(client):
    response = client.post(
        "/api/v1/feedback",
        json={
            "technician_name": "Taylor",
            "feedback_text": "The app will not load my jobs.",
            "score": 6,
        },
    )

    assert response.status_code == 422
