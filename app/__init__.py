from flask import Flask

from .config import Config
from .models import db
from .routes import register_routes


def create_app(config_class: type = Config) -> Flask:
    """Фабрика приложения Flask.

    Args:
        config_class: класс конфигурации, по умолчанию Config.

    Returns:
        Настроенный экземпляр Flask-приложения.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app