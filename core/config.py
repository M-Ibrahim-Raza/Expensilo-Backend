from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database URL
    DATABASE_URL: str

    # App settings
    APP_NAME: str = "Expensilo"
    DEBUG: bool = True


# Instantiate settings
settings = Settings()
