import jwt

from fastapi import Depends
from datetime import datetime, timedelta, timezone
from passlib.hash import bcrypt

from app.core.config import jwt_settings
from app.api.schemas.user import UserInDB


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password_hash(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {**data, "exp": expire}

    return jwt.encode(
        to_encode,
        jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )


if __name__ == "__main__":
    a = hash_password("qwerty123")

    assert verify_password_hash("qwerty123", a)
    assert verify_password_hash("qwesrty123", a) == False

    print(create_access_token(data={"useername": "oleg"}, expires_delta=timedelta(minutes=30)))
