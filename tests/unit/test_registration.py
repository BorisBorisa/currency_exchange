import pytest
from pytest_mock import MockFixture


@pytest.mark.asyncio
async def test_success_registration(mocker: MockFixture, client, override_database_connection, user_register_model):
    mock_register = mocker.patch(
        "app.api.endpoints.registration.register_user_in_db",
        mocker.AsyncMock(return_value=None)
    )

    response = client.post("/auth/register", json=dict(user_register_model))

    assert response.status_code == 201
    assert response.json()["username"] == user_register_model.username
    assert response.json()["message"] == "Пользователь успешно создан"
    mock_register.assert_called_once()
