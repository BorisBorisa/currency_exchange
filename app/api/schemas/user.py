from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date
import re


class User(BaseModel):
    email: EmailStr
    username: str = Field(min_length=2)


class UserRegister(User):
    password: str
    first_name: str
    last_name: str
    birth_date: date

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


class Token(BaseModel):
    access_token: str
    token_type: str


if __name__ == "__main__":
    pass
