from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = ''
    POSTGRES_PORT: int = 0
    POSTGRES_DB: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''

    REDIS_SERVER: str = ''
    REDIS_PORT: int = 0

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
