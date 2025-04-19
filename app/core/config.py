from pathlib import Path
from pydantic_settings import SettingsConfigDict, BaseSettings



class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    model_config = SettingsConfigDict(
        env_file= Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="JWT_",
        case_sensitive=False,
        extra="ignore"
    )


jwt_settings = JWTSettings()