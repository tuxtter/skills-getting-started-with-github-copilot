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
