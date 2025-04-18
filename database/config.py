from pydantic_settings import BaseSettings, SettingsConfigDict


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
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        case_sensitive=False,
        extra="ignore"
    )


settings = DatabaseSettings()

if __name__ == "__main__":
    print(settings.dns)
