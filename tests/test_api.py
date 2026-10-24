def create_workout(client, name="Test Workout"):
    response = client.post(
        "/workouts",
        json={
            "name": name,
            "date": "2026-10-24",
            "notes": "Created by a test",
        },
    )
    assert response.status_code == 201
    return response.get_json()


def create_exercise(client, name="Test Exercise"):
    response = client.post(
        "/exercises",
        json={
            "name": name,
            "description": "Created by a test",
        },
    )
    assert response.status_code == 201
    return response.get_json()


def test_health_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Workout API is running"}


def test_create_and_get_workout(client):
    workout = create_workout(client)

    response = client.get(f"/workouts/{workout['id']}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Workout"


def test_reject_invalid_workout(client):
    response = client.post(
        "/workouts",
        json={"name": "", "date": "2026-10-24"},
    )

    assert response.status_code == 400
    assert "errors" in response.get_json()


def test_create_exercise_and_reject_duplicate(client):
    create_exercise(client)

    response = client.post(
        "/exercises",
        json={
            "name": "Test Exercise",
            "description": "A duplicate",
        },
    )

    assert response.status_code == 409


def test_add_exercise_to_workout(client):
    workout = create_workout(client)
    exercise = create_exercise(client)

    response = client.post(
        f"/workouts/{workout['id']}/exercises",
        json={
            "exercise_id": exercise["id"],
            "sets": 3,
            "reps": 10,
        },
    )

    assert response.status_code == 201
    result = response.get_json()
    assert result["exercises"][0]["exercise"]["name"] == "Test Exercise"
    assert result["exercises"][0]["sets"] == 3
    assert result["exercises"][0]["reps"] == 10


def test_reject_duplicate_exercise_in_workout(client):
    workout = create_workout(client)
    exercise = create_exercise(client)
    payload = {
        "exercise_id": exercise["id"],
        "sets": 3,
        "reps": 10,
    }

    first_response = client.post(
        f"/workouts/{workout['id']}/exercises",
        json=payload,
    )
    second_response = client.post(
        f"/workouts/{workout['id']}/exercises",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_missing_workout_returns_404(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Workout not found."}


def test_missing_exercise_returns_404(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Exercise not found."}
