import pytest


@pytest.fixture
def student(client):
    """Создаёт тестового студента."""
    response = client.post("/students/", json={"name": "Иван", "email": "ivan@mail.ru"})
    return response.get_json()


@pytest.fixture
def subject(client):
    """Создаёт тестовый предмет."""
    response = client.post("/subjects/", json={"name": "Математика"})
    return response.get_json()


def test_list_grades_empty(client):
    """Возвращает пустой список если оценок нет."""
    response = client.get("/grades/")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_grade(client, student, subject):
    """Создаёт оценку и возвращает её данные."""
    response = client.post("/grades/", json={
        "student_id": student["id"],
        "subject_id": subject["id"],
        "value": 85.0,
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["value"] == 85.0
    assert data["student_id"] == student["id"]
    assert data["subject_id"] == subject["id"]


def test_create_grade_missing_fields(client):
    """Возвращает 400 если не переданы обязательные поля."""
    response = client.post("/grades/", json={"value": 85.0})
    assert response.status_code == 400


def test_create_grade_invalid_value(client, student, subject):
    """Возвращает 422 если значение оценки вне диапазона."""
    response = client.post("/grades/", json={
        "student_id": student["id"],
        "subject_id": subject["id"],
        "value": 150.0,
    })
    assert response.status_code == 422


def test_get_grade(client, student, subject):
    """Возвращает оценку по ID."""
    created = client.post("/grades/", json={
        "student_id": student["id"],
        "subject_id": subject["id"],
        "value": 85.0,
    })
    grade_id = created.get_json()["id"]
    response = client.get(f"/grades/{grade_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == grade_id


def test_get_grade_not_found(client):
    """Возвращает 404 если оценка не найдена."""
    response = client.get("/grades/999")
    assert response.status_code == 404


def test_update_grade(client, student, subject):
    """Обновляет значение оценки."""
    created = client.post("/grades/", json={
        "student_id": student["id"],
        "subject_id": subject["id"],
        "value": 85.0,
    })
    grade_id = created.get_json()["id"]
    response = client.put(f"/grades/{grade_id}", json={"value": 90.0})
    assert response.status_code == 200
    assert response.get_json()["value"] == 90.0


def test_delete_grade(client, student, subject):
    """Удаляет оценку и возвращает 204."""
    created = client.post("/grades/", json={
        "student_id": student["id"],
        "subject_id": subject["id"],
        "value": 85.0,
    })
    grade_id = created.get_json()["id"]
    response = client.delete(f"/grades/{grade_id}")
    assert response.status_code == 204
    assert client.get(f"/grades/{grade_id}").status_code == 404