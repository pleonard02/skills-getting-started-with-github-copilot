from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def reset_activity_participants():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_participant_from_activity():
    reset_activity_participants()

    response = client.delete(
        "/activities/Chess Club/unregister?email=daniel@mergington.edu"
    )

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == (
        "Unregistered daniel@mergington.edu from Chess Club"
    )


def test_unregister_missing_participant_returns_404():
    reset_activity_participants()

    response = client.delete(
        "/activities/Chess Club/unregister?email=not-here@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
