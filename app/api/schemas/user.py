from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
import re


class User(BaseModel):
    email: EmailStr
    username: str = Field(min_length=2)


class UserRegister(User):
    password: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if all([
            len(password) >= 8,
            re.search(r"[A-Z]", password),  # Хотя бы 1 заглавная
            re.search(r"[a-z]", password),  # Хотя бы 1 строчная
            re.search(r"\d", password),  # Хотя бы 1 цифра
            re.search(r"[!@#$%^&*]", password)  # Хотя бы 1 спецсимвол
        ]):
            return password

        raise ValueError("Пароль слишком слабый")


class UserInDB(User):
    hashed_password: str
    disabled: bool = False


# Нужно реализовать route который предоставляет информацию о пользователе и возможность эти данные передать
class UserInfo(User):
    birth_date: date
    avatar_url: str
    phone: str
    gender: str


class Token(BaseModel):
    access_token: str
    token_type: str


if __name__ == "__main__":
    pass

