import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original = copy.deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(original)


def test_signup_rejects_duplicate_registration(client):
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    first = client.post(f"/activities/{activity}/signup", params={"email": email})
    second = client.post(f"/activities/{activity}/signup", params={"email": email})

    assert first.status_code == 200
    assert second.status_code == 400
    assert activities[activity]["participants"].count(email) == 1
