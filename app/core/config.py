from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === База данных ===
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "studyhub_user"
    POSTGRES_PASSWORD: str = "studyhub_password"
    POSTGRES_DB: str = "studyhub_db"

    # === JWT ===
    SECRET_KEY: str = "dev-secret-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # === CORS ===
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # === Вычисляемые свойства ===

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def DATABASE_URL_async(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_sync(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ОЧЕНЬ ВАЖНО: extra="ignore" — иначе падает на любой лишней переменной в .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()