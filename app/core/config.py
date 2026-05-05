from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["local", "prod"] = Field(default="local")
    server_port: int = Field(default=8085)
    database_url: str | None = Field(default=None)

    @property
    def effective_database_url(self) -> str:
        if self.app_env == "local":
            return "sqlite:///./employee_local.db"
        if not self.database_url:
            raise RuntimeError(
                "DATABASE_URL must be set when APP_ENV != 'local'"
            )
        return self.database_url

    @property
    def run_migrations_on_startup(self) -> bool:
        return self.app_env != "local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
