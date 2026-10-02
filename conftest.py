import os
import uuid

import pytest
import requests

BASE_URL = os.getenv(
    "STELLAR_BASE_URL",
    "https://stellarburgers.education-services.ru/api",
).rstrip("/")


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


def unique_user():
    suffix = uuid.uuid4().hex[:12]
    return {
        "email": f"api-test-{suffix}@example.com",
        "password": "TestPassword123!",
        "name": f"API Test {suffix}",
    }


@pytest.fixture
def new_user():
    return unique_user()


@pytest.fixture
def registered_user(api_session, new_user):
    response = api_session.post(f"{BASE_URL}/auth/register", json=new_user, timeout=20)
    response.raise_for_status()
    body = response.json()
    assert body.get("success") is True
    return {**new_user, **body.get("user", {})}


@pytest.fixture
def auth_headers(api_session, registered_user):
    token = registered_user["accessToken"]
    return {"Authorization": token}


@pytest.fixture
def valid_ingredients(api_session):
    response = api_session.get(f"{BASE_URL}/ingredients", timeout=20)
    response.raise_for_status()
    body = response.json()
    ingredients = body.get("data", [])
    assert len(ingredients) >= 2, "API should return at least two ingredients"
    return [ingredients[0]["_id"], ingredients[1]["_id"]]


@pytest.fixture
def cleanup_user(api_session):
    created = []
    yield created
    for token in created:
        try:
            api_session.delete(
                f"{BASE_URL}/auth/user",
                headers={"Authorization": token},
                timeout=20,
            )
        except requests.RequestException:
            pass
