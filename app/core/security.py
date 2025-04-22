import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from passlib.hash import bcrypt
from typing import Annotated
from asyncpg import Connection

from config import JWTSettings
from app.api.schemas.user import UserInDB
from db.db_connecion import get_database_connection
from db.queries import get_user_by_username


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(JWTSettings.ACCESS_TOKEN_EXPIRE_MINUTES)
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode = {**data, "exp": expire, "type": "access"}

    return jwt.encode(
        to_encode,
        JWTSettings.SECRET_KEY,
        algorithm=JWTSettings.ALGORITHM
    )


def decode_access_token(token: str):
    return jwt.decode(token, JWTSettings.SECRET_KEY, algorithms=[JWTSettings.ALGORITHM])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        conn: Connection = Depends(get_database_connection),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: dict = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

    except InvalidTokenError as exc:
        raise credentials_exception

    user = await get_user_by_username(conn, username)

    return user


async def get_current_active_user(
        current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


if __name__ == "__main__":
    pass
