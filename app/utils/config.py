from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings


class ExchangeRateAPISettings(BaseSettings):
    API_KEY: str
    BASE_URL: str


    model_config = SettingsConfigDict(
        env_file= Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="ER_",
        case_sensitive=False,
        extra="ignore"
    )


ERAPI_settings = ExchangeRateAPISettings()