import jwt
import pytest

from jwt import InvalidTokenError
from fastapi import HTTPException
from freezegun import freeze_time
from datetime import datetime, timedelta
from pytest_mock import MockFixture
from config import JWT_settings
from app.core import security


def test_hash_password():
    password = "Qwerty123!"

    hashed_password_1 = security.hash_password(password)
    hashed_password_2 = security.hash_password(password)

    assert hashed_password_1 != hashed_password_2
    assert security.verify_password_hash(password, hashed_password_1)


@freeze_time(datetime(2025, 1, 1, 0, 0))
class TestAccessToken:
    KEY = "FAKE_SECRET_KEY"
    ALGORITHM = "HS256"
    TOKEN_EXPIRE = 15
    DATA = {"sub": "test_user"}
    PAYLOAD = {
        **DATA,
        "exp": datetime(2025, 1, 1, 0, 15),
        "type": "access"
    }

    @pytest.fixture(autouse=True)
    def setup_jwt_settings(self, mocker: MockFixture):
        mocker.patch.multiple(
            JWT_settings,
            SECRET_KEY=self.KEY,
            ALGORITHM=self.ALGORITHM,
            ACCESS_TOKEN_EXPIRE_MINUTES=self.TOKEN_EXPIRE
        )

    @pytest.fixture()
    def jwt_token(self):
        return jwt.encode(
            payload=self.PAYLOAD,
            key=self.KEY,
            algorithm=self.ALGORITHM
        )

    def test_create_access_token(self, jwt_token):
        token_default_expiry = security.create_access_token(self.DATA)
        token_custom_expiry = security.create_access_token(self.DATA, timedelta(minutes=15))

        assert token_default_expiry == jwt_token
        assert token_custom_expiry == jwt_token

    def test_decode_access_token(self, jwt_token):
        token = security.decode_access_token(jwt_token)

        assert token["sub"] == "test_user"
        assert token["exp"] == 1735690500
        assert token["type"] == "access"

    def test_expired_token(self):
        token = security.create_access_token(self.DATA, timedelta(minutes=-1))

        with pytest.raises(InvalidTokenError) as exc:
            security.decode_access_token(token)

        assert str(exc.value) == "Signature has expired"

    def test_invalid_signature_token(self):
        token = jwt.encode(
            payload=self.PAYLOAD,
            key="INVALID_SECRET_KEY",
            algorithm=self.ALGORITHM
        )

        with pytest.raises(InvalidTokenError) as exc:
            security.decode_access_token(token)

        assert str(exc.value) == "Signature verification failed"

    def test_invalid_algorithm_token(self):
        token = jwt.encode(
            payload=self.PAYLOAD,
            key=self.KEY,
            algorithm="HS512"
        )

        with pytest.raises(InvalidTokenError) as exc:
            security.decode_access_token(token)

        assert str(exc.value) == "The specified alg value is not allowed"


@pytest.mark.asyncio
async def test_get_current_user(mocker: MockFixture):
    mocker.patch("app.core.security.decode_access_token", return_value={"sub": "test_user"})
    mocker.patch("app.core.security.get_user_by_username", new=mocker.AsyncMock(return_value="test_UserInDB"))

    user = await security.get_current_user("token", mocker.AsyncMock())

    assert user == "test_UserInDB"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mocker: MockFixture):
    mocker.patch("app.core.security.decode_access_token", side_effect=InvalidTokenError())
    mocker.patch("app.core.security.get_user_by_username", new=mocker.AsyncMock(return_value="test_UserInDB"))

    with pytest.raises(HTTPException) as exc:
        await security.get_current_user("token", mocker.AsyncMock())

    assert exc.value.status_code == 401
    assert exc.value.detail == "Не удалось подтвердить учетные данные"


@pytest.mark.asyncio
async def test_get_current_user_missing_user_in_token(mocker: MockFixture):
    mocker.patch("app.core.security.decode_access_token", return_value={})
    mocker.patch("app.core.security.get_user_by_username", new=mocker.AsyncMock(return_value="test_UserInDB"))

    with pytest.raises(HTTPException) as exc:
        await security.get_current_user("token", mocker.AsyncMock())

    assert exc.value.status_code == 401
    assert exc.value.detail == "Не удалось подтвердить учетные данные"


@pytest.mark.asyncio
async def test_get_current_active_user(mocker: MockFixture):
    user = mocker.Mock()
    user.disabled = False

    current_user = await security.get_current_active_user(user)

    assert current_user is user


@pytest.mark.asyncio
async def test_get_current_active_user_raises_if_user_disabled(mocker: MockFixture):
    user = mocker.Mock()
    user.disabled = True

    with pytest.raises(HTTPException) as exc:
        await security.get_current_active_user(user)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Неактивный пользователь"
