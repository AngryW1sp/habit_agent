from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    ENV: str = 'local'
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "habit"
    POSTGRES_PASSWORD: str = "habit"
    POSTGRES_DB: str = "habit_db"

    SQLITE_PATH: str = './habits.db'

    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore'
    )

    @property
    def database_url(self) -> str:
        if self.ENV in ("prod", "staging", "docker"):
            return (
                f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"


settings = Settings()
