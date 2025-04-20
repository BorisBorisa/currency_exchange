from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from asyncpg import Connection
from passlib.exc import InvalidTokenError

from db.db_connecion import get_database_connection
from db.queries import get_user_by_username
from app.api.schemas.user import Token, UserInDB, User
from app.core.security import verify_password_hash, create_access_token, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth = APIRouter()


async def authenticate_user(
        username: str,
        password: str,
        conn: Connection = Depends(get_database_connection)
) -> UserInDB | bool:
    user = await get_user_by_username(conn, username)

    if not user:
        return False

    if not verify_password_hash(password, user.hashed_password):
        return False

    return user


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


@auth.post("/login", summary="эндпоинт для получения токена")
async def login_for_access_token(
        from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        conn: Connection = Depends(get_database_connection)
) -> Token:
    user = await authenticate_user(from_data.username, from_data.password, conn)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Неверное имя пользователя или пароль"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": from_data.username})
    return Token(access_token=access_token, token_type="bearer")


@auth.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
