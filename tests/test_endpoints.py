def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_and_duplicate(client):
    before = len(client.get("/activities").json()["Programming Class"]["participants"])
    # sign up twice with same email (current behavior allows duplicates)
    resp1 = client.post("/activities/Programming%20Class/signup?email=testuser@example.com")
    assert resp1.status_code == 200
    resp2 = client.post("/activities/Programming%20Class/signup?email=testuser@example.com")
    assert resp2.status_code == 200
    after = len(client.get("/activities").json()["Programming Class"]["participants"])
    assert after == before + 2


def test_signup_nonexistent_activity(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == 404


def test_unregister_success(client):
    # michael@mergington.edu is pre-populated in Chess Club
    resp = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert resp.status_code == 200
    assert "Unregistered michael@mergington.edu for Chess Club" in resp.json().get("message", "")


def test_unregister_nonexistent_participant(client):
    resp = client.delete("/activities/Chess%20Club/signup?email=not@there.com")
    assert resp.status_code == 404
