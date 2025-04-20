from fastapi import APIRouter, Depends, status, HTTPException

from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError, PostgresError

from db.db_connecion import get_database_connection
from db.queries import register_user_in_db

from app.api.schemas.user import UserRegister
from app.core.security import hash_password

reg_route = APIRouter(prefix="/auth", tags=["auth"])


@reg_route.post("/register", summary="Регистрация пользователя", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, conn: Connection = Depends(get_database_connection)):

    await register_user_in_db(
        conn,
        user,
        hash_password(user.password)
    )

    return {"message": "Пользователь успешно создан",
            "username": user.username}
