from flask import Blueprint, Response, jsonify, request

from ..models import Student, db

bp = Blueprint("students", __name__)

@bp.get("/")
def list_students() -> Response:
    """Возвращает список всех студентов."""
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@bp.get("/<int:student_id>")
def get_student(student_id: int) -> Response:
    """Возвращает студента по ID.

    Args:
        student_id: идентификатор студента.
    """
    student = Student.query.get_or_404(student_id)
    return jsonify(student.to_dict())


@bp.post("/")
def create_student() -> tuple[Response, int]:
    """Создаёт нового студента.

    Body: {"name": str, "email": str}
    """
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    if Student.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already exists"}), 409

    student = Student(name=data["name"], email=data["email"])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@bp.put("/<int:student_id>")
def update_student(student_id: int) -> Response:
    """Обновляет данные студента.

    Args:
        student_id: идентификатор студента.
    """
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    if "name" in data:
        student.name = data["name"]
    if "email" in data:
        student.email = data["email"]
    db.session.commit()
    return jsonify(student.to_dict())


@bp.delete("/<int:student_id>")
def delete_student(student_id: int) -> tuple[str, int]:
    """Удаляет студента по ID.

    Args:
        student_id: идентификатор студента.
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return "", 204