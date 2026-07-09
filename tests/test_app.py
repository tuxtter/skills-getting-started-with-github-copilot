<<<<<<< HEAD
from fastapi.testclient import TestClient

from src import app as app_module


def test_unregister_participant_removes_their_email():
    client = TestClient(app_module.app)
    activity_name = "Chess Club"
    email = "student@example.edu"

    app_module.activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
=======
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities
from src.app import app as fastapi_app


@pytest.fixture
def client():
    return TestClient(fastapi_app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    original = deepcopy(activities)
    activities.clear()
    activities.update(deepcopy(original))
    yield
    activities.clear()
    activities.update(deepcopy(original))


def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_catalog(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert "participants" in payload["Chess Club"]


def test_signup_for_activity_appends_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Programming Class"
    assert email in activities["Programming Class"]["participants"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
>>>>>>> 8cd3b54 (test added)
