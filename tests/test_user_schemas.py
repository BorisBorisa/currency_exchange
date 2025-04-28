import pytest
from pydantic import ValidationError
from app.api.schemas import user
from tests.test_data import correct_passwords, invalid_passwords, invalid_emails


@pytest.mark.parametrize("password", correct_passwords)
def test_correct_passwords(password: str):
    user.UserRegister(
        email="test@gmail.com",
        username="test",
        password=password,
    )


@pytest.mark.parametrize("password", invalid_passwords)
def test_incorrect_passwords(password: str):
    with pytest.raises(ValueError):
        user.UserRegister(
            email="test@gmail.com",
            username="test",
            password=password,
        )


def test_user():
    model = user.User(
        email="test@gmail.com",
        username="qe"
    )

    assert model.email == "test@gmail.com"
    assert model.username == "qe"



@pytest.mark.parametrize("username", (
    "1", 1, 1.2, "A"
))
def test_user_invalid_username(username):
    with pytest.raises(ValidationError):
        user.User(
            email="test@gmail.com",
            username=username
        )


@pytest.mark.parametrize("mail", invalid_emails)
def test_user_invalid_username(mail):
    with pytest.raises(ValidationError):
        user.User(
            email=mail,
            username="username"
        )


def test_user_in_db():
    model = user.UserInDB(
        email="test@gmail.com",
        username="test",
        hashed_password="hashed_password_asdasd"
    )

    assert model.hashed_password == "hashed_password_asdasd"
    assert model.disabled == False


