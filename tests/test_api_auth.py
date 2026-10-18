"""Security regression tests for the Enterprise API auth gate."""
from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health_does_not_require_token(monkeypatch):
    monkeypatch.delenv("BE_API_TOKEN", raising=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["authenticated_api_configured"] is False


def test_stateful_routes_fail_closed_when_token_missing(monkeypatch):
    monkeypatch.delenv("BE_API_TOKEN", raising=False)
    response = client.post(
        "/onboarding/start",
        json={"company_name": "Example", "assistant_name": "Assistant"},
    )
    assert response.status_code == 503


def test_stateful_routes_reject_missing_or_invalid_token(monkeypatch):
    monkeypatch.setenv("BE_API_TOKEN", "test-secret-token")
    payload = {"company_name": "Example", "assistant_name": "Assistant"}
    assert client.post("/onboarding/start", json=payload).status_code == 401
    assert client.post(
        "/onboarding/start",
        json=payload,
        headers={"Authorization": "Bearer incorrect"},
    ).status_code == 401


def test_valid_token_allows_onboarding_and_context(monkeypatch):
    monkeypatch.setenv("BE_API_TOKEN", "test-secret-token")
    headers = {"Authorization": "Bearer test-secret-token"}
    response = client.post(
        "/onboarding/start",
        json={"company_name": "Regression Test Company", "assistant_name": "Test Helper"},
        headers=headers,
    )
    assert response.status_code == 200
    assistant_id = response.json()["assistant_id"]
    context = client.get(f"/onboarding/{assistant_id}/context", headers=headers)
    assert context.status_code == 200
    assert context.json()["company_id"] == "new"
