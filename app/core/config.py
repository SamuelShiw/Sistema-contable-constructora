from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_env: str
    app_version: str

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    database_url_env: str | None = None

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        database_url = getattr(self, "database_url_env", None)

        if database_url:
            return database_url

        return (
            f"postgresql+psycopg://{self.database_user}:"
            f"{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()