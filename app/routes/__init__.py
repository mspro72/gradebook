from flask import Flask

from .grades import bp as grades_bp
from .stats import bp as stats_bp
from .students import bp as students_bp
from .subjects import bp as subjects_bp


def register_routes(app: Flask) -> None:
    """Регистрирует все blueprint-ы в приложении.

    Args:
        app: экземпляр Flask-приложения.
    """
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(subjects_bp, url_prefix="/subjects")
    app.register_blueprint(grades_bp, url_prefix="/grades")
    app.register_blueprint(stats_bp, url_prefix="/stats")