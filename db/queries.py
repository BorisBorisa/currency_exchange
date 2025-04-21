from asyncpg import Connection
from asyncpg.exceptions import PostgresError, UniqueViolationError
from fastapi import HTTPException, status

from app.api.schemas.user import UserInDB, UserRegister


async def get_user_by_username(conn: Connection, username: str) -> UserInDB | None:
    try:
        user = await conn.fetchrow(
            "SELECT username, email, password_hash, disabled FROM users WHERE username = $1",
            username
        )
    except PostgresError as exc:
        print(exc)  # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if user:
        return UserInDB(
            username=user["username"],
            email=user["email"],
            disabled=user["disabled"],
            hashed_password=user["password_hash"]
        )


async def register_user_in_db(conn: Connection, user: UserRegister, hashed_password: str) -> None:
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
        print(exc)  # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email или username уже существует"
        )

    except PostgresError as exc:
        print(exc)  # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при регистрации"
        )


async def get_supported_currencies(conn: Connection) -> dict:
    try:
        currencies = await conn.fetch(
            "SELECT currency_code, currency_name FROM currencies",
        )

    except PostgresError as exc:
        print(exc)  # Добавить логирование
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    return dict(currencies)
