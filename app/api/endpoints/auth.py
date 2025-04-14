from fastapi import APIRouter

from app.api.schemas.user import UserRegister

auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.post("/register", summary="Регистрация пользователя")
async def register(user: UserRegister):


# проверить отсутствие в бд такого имени пользователя и почты
# хешировать пароль
# создать пользователя
# сохранение в БД

    return {"message": "Пользователь успешно создан",
            "username": user.username}


@auth_route.post("/login", summary="Авторизация пользователя")
async def login():
    pass
