from passlib.hash import bcrypt
from passlib.exc import PasswordTruncateError


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password_hash(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


if __name__ == "__main__":
    pass
