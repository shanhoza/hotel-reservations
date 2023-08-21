from re import S

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
