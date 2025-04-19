from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from asyncpg import Connection

from db.db_connecion import get_database_connection
from db.queries import get_user_by_username
from app.api.schemas.user import Token, UserInDB
from app.core.security import verify_password_hash, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth = APIRouter()


@auth.post("/login", summary="эндпоинт для получения токена")
async def authorization(
        from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        conn: Connection = Depends(get_database_connection)
) -> Token:

    user: UserInDB = await get_user_by_username(conn, from_data.username)
    pass_valid: bool = verify_password_hash(from_data.password, user["password_hash"])

    if not (user and pass_valid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Неверное имя пользователя или пароль"},
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(data={"sub": from_data.username})

    return Token(access_token=access_token)
