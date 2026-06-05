import pytest

def test_list_students_empty(client):
    """Возвращает пустой список если студентов нет."""
    response = client.get("/students/")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_student(client):
    """Создаёт студента и возвращает его данные."""
    response = client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Иван"
    assert data["email"] == "ivan@mail.ru"
    assert "id" in data


def test_create_student_missing_fields(client):
    """Возвращает 400 если не переданы обязательные поля."""
    response = client.post("/students/", json={"name": "Иван"})
    assert response.status_code == 400


def test_create_student_duplicate_email(client):
    """Возвращает 409 если email уже существует."""
    client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    response = client.post("/students/", json={"name": "Другой", "email": "ivan@mail.ru"})
    assert response.status_code == 409


def test_get_student(client):
    """Возвращает студента по ID."""
    created = client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    student_id = created.get_json()["id"]
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == student_id


def test_get_student_not_found(client):
    """Возвращает 404 если студент не найден."""
    response = client.get("/students/999")
    assert response.status_code == 404


def test_update_student(client):
    """Обновляет имя студента."""
    created = client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    student_id = created.get_json()["id"]
    response = client.put(f"/students/{student_id}", json={"name": "Пётр"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Пётр"


def test_delete_student(client):
    """Удаляет студента и возвращает 204."""
    created = client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    student_id = created.get_json()["id"]
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204
    assert client.get(f"/students/{student_id}").status_code == 404