from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''

    REDIS_SERVER: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    RABBITMQ_SERVER: str = '127.0.0.1'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_DEFAULT_USER: str = ''
    RABBITMQ_DEFAULT_PASS: str = ''
    RABBITMQ_DEFAULT_VHOST: str = ''

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
