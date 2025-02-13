# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dbConnection.mongoRepository import get_database

@pytest.fixture(scope="session")
def test_app():
    return app

@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)

@pytest.fixture(scope="session")
def test_db():
    db = get_database()
    app.state.db = db
    return db