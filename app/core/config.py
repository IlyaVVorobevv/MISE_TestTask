from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()