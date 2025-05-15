import pytest

import app.api.endpoints.auth
from app.api.endpoints.auth import authenticate_user
from pytest_mock import MockFixture
from fastapi.security import OAuth2PasswordRequestForm


@pytest.mark.asyncio
async def test_authenticate_user(user_register_model, user_in_db_model, mocker: MockFixture, conn):
    mocker.patch(
        "app.api.endpoints.auth.get_user_by_username",
        new=mocker.AsyncMock(return_value=user_in_db_model)
    )
    mocker.patch(
        "app.api.endpoints.auth.verify_password_hash",
        return_value=True
    )

    user = await authenticate_user(user_register_model.username, user_register_model.password, conn)

    assert user is user_in_db_model


@pytest.mark.asyncio
async def test_authenticate_user_when_user_not_found(user_register_model, mocker: MockFixture, conn):
    mocker.patch(
        "app.api.endpoints.auth.get_user_by_username",
        new=mocker.AsyncMock(return_value=None)
    )

    user = await authenticate_user(user_register_model.username, user_register_model.password, conn)

    assert user is False


@pytest.mark.asyncio
async def test_authenticate_user_when_invalid_pass(user_register_model, user_in_db_model, mocker: MockFixture, conn):
    mocker.patch(
        "app.api.endpoints.auth.get_user_by_username",
        new=mocker.AsyncMock(return_value=user_in_db_model)
    )
    mocker.patch(
        "app.api.endpoints.auth.verify_password_hash",
        return_value=False
    )

    user = await authenticate_user(user_register_model.username, user_register_model.password, conn)

    assert user is False


@pytest.mark.asyncio
async def test_login_route(client, override_login_form, override_database_connection, mocker: MockFixture,
                           user_in_db_model):
    mocker.patch(
        "app.api.endpoints.auth.authenticate_user",
        mocker.AsyncMock(return_value=user_in_db_model)
    )
    mocker.patch(
        "app.api.endpoints.auth.create_access_token",
        return_value="test_access_token"
    )

    response = client.post("/login")

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] == "test_access_token"


@pytest.mark.asyncio
async def test_login_when_user_not_authenticated(
        client,
        override_login_form,
        override_database_connection,
        mocker: MockFixture,
):
    mocker.patch(
        "app.api.endpoints.auth.authenticate_user",
        mocker.AsyncMock(return_value=False)
    )

    response = client.post("/login")

    assert response.status_code == 401
    assert response.json()["detail"] == {"message": "Неверное имя пользователя или пароль"}
    assert response.headers.get("WWW-Authenticate") == "Bearer"

