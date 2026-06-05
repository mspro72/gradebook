import pytest

from app import create_app
from app.config import TestingConfig
from app.models import db as _db


@pytest.fixture(scope="session")
def app():
    """Создаёт тестовое Flask-приложение."""
    app = create_app(TestingConfig)
    return app


@pytest.fixture(scope="session")
def client(app):
    """Создаёт тестовый HTTP-клиент."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Очищает базу данных перед каждым тестом."""
    with app.app_context():
        _db.create_all()
        yield
        _db.session.remove()
        _db.drop_all()