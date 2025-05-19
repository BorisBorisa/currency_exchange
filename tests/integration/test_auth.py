import pytest
from tests.conftest import client


@pytest.mark.asyncio
async def test_successful_login(client, user_register_model, create_test_user):
    with client:
        response = client.post("/login", data={"username": user_register_model.username,
                                               "password": user_register_model.password})

        assert response.status_code == 200
        assert response.json()["access_token"]
        assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_invalid_password(client, user_register_model, create_test_user):
    with client:
        response = client.post("/login", data={"username": user_register_model.username,
                                               "password": ""})


        assert response.status_code == 401
        assert response.json()["detail"] == {"message": "Неверное имя пользователя или пароль"}
        assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.asyncio
async def test_login_with_invalid_password(client, user_register_model, create_test_user):
    with client:
        response = client.post("/login", data={"username": "",
                                               "password": user_register_model.password})

        assert response.status_code == 401
        assert response.json()["detail"] == {"message": "Неверное имя пользователя или пароль"}
        assert response.headers["WWW-Authenticate"] == "Bearer"