from fastapi import APIRouter, Depends, status, HTTPException
from asyncpg import Connection, exceptions


from asyncpg.exceptions import UniqueViolationError
from app.database import get_connection

from app.api.schemas.user import UserRegister
from app.core.security import hash_password, verify_password_hash

auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/register", summary="Регистрация пользователя", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, conn: Connection = Depends(get_connection)):
    hashed_password = hash_password(user.password)

    try:
        async with conn.transaction():
            user_id = await conn.fetchval(
                "INSERT INTO users(username, email, password_hash) VALUES($1, $2, $3) RETURNING id",
                user.username,
                user.email,
                hashed_password
            )

            await conn.execute(
                "INSERT INTO user_profiles(id, first_name, last_name, birth_date) VALUES($1, $2, $3, $4)",
                user_id,
                user.first_name,
                user.last_name,
                user.birth_date
            )
    except UniqueViolationError as exc:
        print(exc) # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email или username уже существует"
        )
    except Exception as exc:
        print(exc) # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при регистрации"
        )


    return {"message": "Пользователь успешно создан",
            "username": user.username}



@auth_route.post("/login", summary="Авторизация пользователя")
async def login():
    pass
