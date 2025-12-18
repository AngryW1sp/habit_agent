"""Конфигурация приложения: настройки окружения и генерация URL для БД и Redis."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения (загружаются из окружения или .env файла)."""

    ENV: str = "local"

    # SQLite (local)
    SQLITE_PATH: str = "./habits.db"

    # Postgres
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "habit"
    POSTGRES_PASSWORD: str = "habit"
    POSTGRES_DB: str = "habit_db"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        """URL подключения к базе данных, формируется на основе настроек окружения."""
        if self.ENV == "local":
            return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        """URL подключения к Redis на основе настроек."""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


settings = Settings()
