from flask import Blueprint, Response, jsonify, request

from ..models import Subject, db

bp = Blueprint("subjects", __name__)

@bp.get("/")
def list_subjects() -> Response:
    """Возвращает список всех предметов"""
    return jsonify([s.to_dict() for s in Subject.query.all()])


@bp.get("/<int:subject_id>")
def get_subject(subject_id: int) -> Response:
    """Возвращает предмет по ID

    Args:
        subject_id: идентификатор предмета
    """
    subject = Subject.query.get_or_404(subject_id)
    return jsonify(subject.to_dict())


@bp.post("/")
def create_subject() -> tuple[Response, int]:
    """Создаёт новый предмет

    Body: {"name": str}
    """
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    if Subject.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "subject already exists"}), 409

    subject = Subject(name=data["name"])
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_dict()), 201


@bp.put("/<int:subject_id>")
def update_subject(subject_id: int) -> Response:
    """Обновляет название предмета

    Args:
        subject_id: идентификатор предмета
    """
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json()
    if "name" in data:
        subject.name = data["name"]
    db.session.commit()
    return jsonify(subject.to_dict())


@bp.delete("/<int:subject_id>")
def delete_subject(subject_id: int) -> tuple[str, int]:
    """Удаляет предмет по ID

    Args:
        subject_id: идентификатор предмета
    """
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return "", 204