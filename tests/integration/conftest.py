import pytest
import asyncpg
import pytest_asyncio
from unittest.mock import AsyncMock

from app.api.endpoints.currency import get_current_active_user
from app.api.schemas.user import User, UserRegister
from app.core.security import hash_password
from db.db_connecion import DB_settings
from db.queries import register_user_in_db


@pytest.fixture()
def override_get_current_active_user(client):
    client.app.dependency_overrides[get_current_active_user] = lambda: AsyncMock()
    yield
    client.app.dependency_overrides.clear()


@pytest.fixture()
def user_model():
    return User(
        email="test@example.com",
        username="test_name"
    )


@pytest.fixture()
def user_register_model(user_model):
    return UserRegister(
        **dict(user_model),
        password="Qwerty1!"
    )


@pytest_asyncio.fixture()
async def database_connect():
    connect = await asyncpg.connect(dsn=DB_settings.dns)
    try:
        yield connect
    finally:
        await connect.close()


@pytest_asyncio.fixture()
async def create_test_user(database_connect, user_register_model):
    try:
        await register_user_in_db(
            database_connect,
            user_register_model,
            hash_password(user_register_model.password)
        )
        yield
    finally:
        await database_connect.fetch("DELETE FROM users WHERE username = $1", user_register_model.username)
