from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg import Connection


from db.db_connecion import get_database_connection
from db.queries import get_user_by_username
from app.api.schemas.user import Token, UserInDB
from app.core.security import  create_access_token, verify_password_hash

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


@auth.post("/login", summary="Эндпоинт для получения токена", tags=["tokenUrl"])
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
