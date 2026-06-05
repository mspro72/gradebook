def test_list_subjects_empty(client):
    """Возвращает пустой список если предметов нет."""
    response = client.get("/subjects/")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_subject(client):
    """Создаёт предмет и возвращает его данные."""
    response = client.post("/subjects/", json={"name": "Математика"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Математика"
    assert "id" in data


def test_create_subject_missing_fields(client):
    """Возвращает 400 если не передано название."""
    response = client.post("/subjects/", json={})
    assert response.status_code == 400


def test_create_subject_duplicate(client):
    """Возвращает 409 если предмет уже существует."""
    client.post("/subjects/", json={"name": "Математика"})
    response = client.post("/subjects/", json={"name": "Математика"})
    assert response.status_code == 409


def test_get_subject(client):
    """Возвращает предмет по ID."""
    created = client.post("/subjects/", json={"name": "Математика"})
    subject_id = created.get_json()["id"]
    response = client.get(f"/subjects/{subject_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == subject_id


def test_get_subject_not_found(client):
    """Возвращает 404 если предмет не найден."""
    response = client.get("/subjects/999")
    assert response.status_code == 404


def test_update_subject(client):
    """Обновляет название предмета."""
    created = client.post("/subjects/", json={"name": "Математика"})
    subject_id = created.get_json()["id"]
    response = client.put(f"/subjects/{subject_id}", json={"name": "Физика"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Физика"


def test_delete_subject(client):
    """Удаляет предмет и возвращает 204."""
    created = client.post("/subjects/", json={"name": "Математика"})
    subject_id = created.get_json()["id"]
    response = client.delete(f"/subjects/{subject_id}")
    assert response.status_code == 204
    assert client.get(f"/subjects/{subject_id}").status_code == 404