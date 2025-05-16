import pytest
from fastapi.testclient import TestClient

from db.db_connecion import get_database_connection
from unittest.mock import AsyncMock

from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture()
def override_database_connection(client):
    client.app.dependency_overrides[get_database_connection] = lambda: AsyncMock()
    yield
    client.app.dependency_overrides.clear()


if __name__ == "__main__":
    pass
