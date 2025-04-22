import asyncio

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from asyncpg import create_pool, Pool

from config import db_settings as settings


# Инициализация и закрытие пула
@asynccontextmanager
async def lifespan(app: FastAPI):
    connection_pool = await create_pool(
        dsn=settings.dns,
        min_size=settings.POOL_MIN,
        max_size=settings.POOL_MAX,
        command_timeout=settings.POOL_TIMEOUT,
        server_settings={
            'search_path': settings.SCHEMA
        }
    )

    app.state.connection_pool = connection_pool
    yield
    await app.state.connection_pool.close()


# генератор используется как dependency для получения соединения из пула
async def get_database_connection(request: Request):
    async with request.app.state.connection_pool.acquire() as conn:
        yield conn


if __name__ == "__main__":
    async def test_db_connection():
        app = FastAPI()

        async with lifespan(app):
            assert app.state.connection_pool is not None
            assert not app.state.connection_pool._closed

            async with app.state.connection_pool.acquire() as conn:
                print(await conn.fetchrow("SELECT current_database();"))
                print(await conn.fetchrow("SELECT current_schema();"))

                print(await conn.fetchval("SELECT EXISTS(SELECT 1)"))


    asyncio.run(test_db_connection())
