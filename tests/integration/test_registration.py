import pytest
from tests.conftest import client


@pytest.mark.asyncio
async def test_success_registration(client, user_register_model, database_connect):
    with client:
        try:
            response = client.post("/auth/register", json=dict(user_register_model))
            assert response.status_code == 201
            assert response.json()["username"] == user_register_model.username
            assert response.json()["message"] == "Пользователь успешно создан"
        finally:
            await database_connect.fetch("DELETE FROM users WHERE username = $1", user_register_model.username)



@pytest.mark.asyncio
async def test_existing_user_registration(client, user_register_model, create_test_user):
    with client:
        response = client.post("/auth/register", json=dict(user_register_model))

        assert response.status_code == 409
        assert response.json()["detail"] == "Пользователь с таким email или username уже существует"