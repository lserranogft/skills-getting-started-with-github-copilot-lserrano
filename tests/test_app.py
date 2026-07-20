def test_root_redirects_to_static_index(client):
    # Arrange
    # No special setup is required for the root route.

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()

    assert expected_activity in payload
    assert payload[expected_activity]["max_participants"] == 12
    assert "michael@mergington.edu" in payload[expected_activity]["participants"]


def test_signup_adds_new_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Signed up {email} for Programming Class"

    activities_response = client.get("/activities")
    activities_payload = activities_response.json()
    assert email in activities_payload["Programming Class"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_removes_existing_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities_response = client.get("/activities")
    activities_payload = activities_response.json()
    assert email not in activities_payload["Chess Club"]["participants"]


def test_unregister_returns_404_for_unknown_participant(client):
    # Arrange
    unknown_email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{unknown_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
