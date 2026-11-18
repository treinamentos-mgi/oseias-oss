from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_names = set(activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json()) == expected_names
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Art Studio/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Studio"}
    assert email in activities["Art Studio"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": "a@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400_and_does_not_add_again(client):
    # Arrange
    email = "michael@mergington.edu"
    participants_before = list(activities["Chess Club"]["participants"])

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities["Chess Club"]["participants"] == participants_before


def test_cancel_signup_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 204
    assert response.content == b""
    assert email not in activities["Chess Club"]["participants"]


def test_cancel_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": "a@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_cancel_signup_not_registered_returns_404(client):
    # Arrange
    email = "not.signed.up@mergington.edu"
    participants_before = list(activities["Chess Club"]["participants"])

    # Act
    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
    assert activities["Chess Club"]["participants"] == participants_before
