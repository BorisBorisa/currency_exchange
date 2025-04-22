from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings


class DatabaseSettings(BaseSettings):
    # Параметры подключения
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str
    SCHEMA: str

    # Настройки пула соединений
    POOL_MIN: int
    POOL_MAX: int
    POOL_TIMEOUT: int

    @property
    def dns(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        case_sensitive=False,
        extra="ignore"
    )


class ExchangeRateAPISettings(BaseSettings):
    API_KEY: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="ER_",
        case_sensitive=False,
        extra="ignore"
    )


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="JWT_",
        case_sensitive=False,
        extra="ignore"
    )


jwt_settings = JWTSettings()
ERAPI_settings = ExchangeRateAPISettings()
db_settings = DatabaseSettings()

if __name__ == "__main__":
    print(db_settings.dns)
