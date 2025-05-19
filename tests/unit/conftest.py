import pytest
from pytest_mock import MockFixture
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.user import User, UserRegister, UserInDB


@pytest.fixture()
def override_login_form(client, oauth2_request_form):
    def mock_oauth_form():
        return oauth2_request_form

    client.app.dependency_overrides[OAuth2PasswordRequestForm] = mock_oauth_form
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


@pytest.fixture()
def user_in_db_model(user_model):
    return UserInDB(
        **dict(user_model),
        hashed_password="pass_hash",
        disabled=False
    )


@pytest.fixture()
def conn(mocker: MockFixture):
    return mocker.AsyncMock()


if __name__ == "__main__":
    pass
