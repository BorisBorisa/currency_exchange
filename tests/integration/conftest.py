import pytest
from unittest.mock import AsyncMock
from app.api.endpoints.currency import get_current_active_user


@pytest.fixture()
def override_get_current_active_user(client):
    client.app.dependency_overrides[get_current_active_user] = lambda: AsyncMock()
    yield
    client.app.dependency_overrides.clear()