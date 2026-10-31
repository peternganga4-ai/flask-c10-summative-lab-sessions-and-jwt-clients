def test_user_can_signup(client):
    response = client.post("/signup", json={
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    })

    assert response.status_code == 201
    assert response.json["user"]["username"] == "peter"
    assert "token" in response.json


def test_signup_rejects_duplicate_username(client):
    user_data = {
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    }

    client.post("/signup", json=user_data)
    response = client.post("/signup", json=user_data)

    assert response.status_code == 409


def test_signup_rejects_password_mismatch(client):
    response = client.post("/signup", json={
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Different123!"
    })

    assert response.status_code == 400


def test_user_can_login(client):
    client.post("/signup", json={
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    })

    response = client.post("/login", json={
        "username": "peter",
        "password": "Password123!"
    })

    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["user"]["username"] == "peter"


def test_login_rejects_wrong_password(client):
    client.post("/signup", json={
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    })

    response = client.post("/login", json={
        "username": "peter",
        "password": "WrongPassword123!"
    })

    assert response.status_code == 401


def test_authenticated_user_can_access_me(client):
    signup_response = client.post("/signup", json={
        "username": "peter",
        "password": "Password123!",
        "password_confirmation": "Password123!"
    })

    token = signup_response.json["token"]

    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json["username"] == "peter"


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401