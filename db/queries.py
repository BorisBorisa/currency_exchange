from asyncpg import Connection

from app.api.schemas.user import UserInDB, UserRegister


async def get_user_by_username(conn: Connection, username: str) -> UserInDB:
    user = await conn.fetchrow(
        "SELECT username, email, password_hash, disabled FROM users WHERE username = $1",
        username
    )

    return UserInDB(
        username=user["username"],
        email=user["email"],
        disabled=user["disabled"],
        hashed_password=user["password_hash"]
    )


async def register_user_in_db(conn: Connection, user: UserRegister, hashed_password: str) -> None:
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
