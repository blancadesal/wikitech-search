import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.api import summaries
from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


def create_test_client(app):
    app.dependency_overrides[get_settings] = get_settings_override
    return TestClient(app)


def register_tortoise_for_test(app):
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@pytest.fixture(scope="module")
def test_app():
    app = create_application()
    test_client = create_test_client(app)
    with test_client as test_client_instance:
        yield test_client_instance


@pytest.fixture(scope="module")
def test_app_with_db():
    app = create_application()
    register_tortoise_for_test(app)
    test_client = create_test_client(app)
    with test_client as test_client_instance:
        yield test_client_instance


@pytest.fixture
def mock_generate_summary(monkeypatch):
    def generate_summary(id, url):
        return None

    monkeypatch.setattr(summaries, "generate_summary", generate_summary)
    return generate_summary
