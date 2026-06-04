from flask import Blueprint, Response, jsonify, request

from ..models import Grade, Student, Subject, db

bp = Blueprint("grades", __name__)

@bp.get("/")
def list_grades() -> Response:
    """Возвращает список всех оценок"""
    return jsonify([g.to_dict() for g in Grade.query.all()])


@bp.get("/<int:grade_id>")
def get_grade(grade_id: int) -> Response:
    """Возвращает оценку по ID

    Args:
        grade_id: идентификатор оценки.
    """
    grade = Grade.query.get_or_404(grade_id)
    return jsonify(grade.to_dict())


@bp.post("/")
def create_grade() -> tuple[Response, int]:
    """Создаёт новую оценку

    Body: {"student_id": int, "subject_id": int, "value": float}
    """
    data = request.get_json()
    required = ("student_id", "subject_id", "value")
    if not data or not all(k in data for k in required):
        return jsonify({"error": "student_id, subject_id and value are required"}), 400

    value = data["value"]
    if not isinstance(value, (int, float)) or not (0 <= value <= 100):
        return jsonify({"error": "value must be a number between 0 and 100"}), 422

    Student.query.get_or_404(data["student_id"])
    Subject.query.get_or_404(data["subject_id"])

    grade = Grade(
        student_id=data["student_id"],
        subject_id=data["subject_id"],
        value=float(value),
    )
    db.session.add(grade)
    db.session.commit()
    return jsonify(grade.to_dict()), 201


@bp.put("/<int:grade_id>")
def update_grade(grade_id: int) -> Response:
    """Обновляет значение оценки

    Args:
        grade_id: идентификатор оценки.
    """
    grade = Grade.query.get_or_404(grade_id)
    data = request.get_json()
    if "value" in data:
        value = data["value"]
        if not isinstance(value, (int, float)) or not (0 <= value <= 100):
            return jsonify({"error": "value must be between 0 and 100"}), 422
        grade.value = float(value)
    db.session.commit()
    return jsonify(grade.to_dict())


@bp.delete("/<int:grade_id>")
def delete_grade(grade_id: int) -> tuple[str, int]:
    """Удаляет оценку по ID.

    Args:
        grade_id: идентификатор оценки.
    """
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    return "", 204