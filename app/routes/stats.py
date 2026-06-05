from flask import Blueprint, Response, jsonify

from ..models import Grade, Student, Subject
from gradebook_core.stats import mean, median, min_grade, max_grade

bp = Blueprint("stats", __name__)

def _get_values(grades: list[Grade]) -> list[float]:
    """Извлекает числовые значения из списка оценок

    Args:
        grades: список объектов Grade

    Returns:
        Список числовых значений оценок
    """
    return [g.value for g in grades]


def _build_stats(values: list[float]) -> dict | None:
    """Вычисляет статистику по списку значений

    Args:
        values: список числовых значений

    Returns:
        Словарь со статистикой или None если список пустой
    """
    if not values:
        return None
    return {
        "mean": mean(values),
        "median": median(values),
        "min": min_grade(values),
        "max": max_grade(values),
        "count": len(values),
    }


@bp.get("/student/<int:student_id>")
def stats_by_student(student_id: int) -> Response:
    """Возвращает статистику оценок студента

    Args:
        student_id: идентификатор студента
    """
    Student.query.get_or_404(student_id)
    values = _get_values(Grade.query.filter_by(student_id=student_id).all())
    result = _build_stats(values)
    if result is None:
        return jsonify({"message": "no grades found"}), 404
    return jsonify(result)


@bp.get("/subject/<int:subject_id>")
def stats_by_subject(subject_id: int) -> Response:
    """Возвращает статистику оценок по предмету

    Args:
        subject_id: идентификатор предмета
    """
    Subject.query.get_or_404(subject_id)
    values = _get_values(Grade.query.filter_by(subject_id=subject_id).all())
    result = _build_stats(values)
    if result is None:
        return jsonify({"message": "no grades found"}), 404
    return jsonify(result)