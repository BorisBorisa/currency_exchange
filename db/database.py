from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import settings

from asyncpg import create_pool, Pool


pool: Pool = None

# Инициализация и закрытие пула
@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await create_pool(
        dsn=settings.dns,
        min_size=settings.POOL_MIN,
        max_size=settings.POOL_MAX,
        command_timeout=settings.POOL_TIMEOUT,
        server_settings = {
            'search_path': settings.SCHEMA
        }
    )
    yield
    await pool.close()


# генератор используется как dependency для получения соединения из пула
async def get_db():
    async with pool.acquire() as conn:
        yield conn



if __name__ == "__main__":
    pass


