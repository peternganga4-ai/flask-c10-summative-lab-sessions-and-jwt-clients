def create_user_and_get_token(client, username="peter"):
    response = client.post("/signup", json={
        "username": username,
        "password": "Password123!",
        "password_confirmation": "Password123!"
    })

    return response.json["token"]


def create_note(client, token):
    return client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "My First Note",
            "content": "Learning Flask testing."
        }
    )


def test_user_can_create_note(client):
    token = create_user_and_get_token(client)

    response = create_note(client, token)

    assert response.status_code == 201
    assert response.json["title"] == "My First Note"


def test_user_can_get_all_notes(client):
    token = create_user_and_get_token(client)
    create_note(client, token)

    response = client.get(
        "/notes",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json["notes"]) == 1


def test_user_can_get_single_note(client):
    token = create_user_and_get_token(client)
    note = create_note(client, token)

    note_id = note.json["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json["title"] == "My First Note"


def test_user_can_update_note(client):
    token = create_user_and_get_token(client)
    note = create_note(client, token)

    note_id = note.json["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated Note"}
    )

    assert response.status_code == 200
    assert response.json["title"] == "Updated Note"


def test_user_can_delete_note(client):
    token = create_user_and_get_token(client)
    note = create_note(client, token)

    note_id = note.json["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_deleted_note_returns_404(client):
    token = create_user_and_get_token(client)
    note = create_note(client, token)

    note_id = note.json["id"]

    client.delete(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_note(client):
    peter_token = create_user_and_get_token(client, "peter")
    second_user_token = create_user_and_get_token(client, "seconduser")

    note = create_note(client, peter_token)
    note_id = note.json["id"]

    response = client.get(
        f"/notes/{note_id}",
        headers={"Authorization": f"Bearer {second_user_token}"}
    )

    assert response.status_code == 404


def test_notes_require_authentication(client):
    response = client.get("/notes")

    assert response.status_code == 401