from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class TypeEnum(str, Enum):
    no_set = ''
    file = 'FILE'
    sheet = 'SHEET'


class Settings(BaseSettings):
    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''

    REDIS_SERVER: str = '127.0.0.1'
    REDIS_PORT: int = 6379
    CACHE_LIFETIME: int = 5

    RABBITMQ_SERVER: str = '127.0.0.1'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_DEFAULT_USER: str = ''
    RABBITMQ_DEFAULT_PASS: str = ''
    RABBITMQ_DEFAULT_VHOST: str = ''

    PATH_TO_STORE: str = ''

    EXCHANGE_SCHEDULE: int = 15
    EXCHANGE_TYPE: TypeEnum = TypeEnum.no_set
    EXCHANGE_FILE: str = ''
    EXCHANGE_SHEET_ID: str = ''
    EXCHANGE_SHEET_TOKEN: str = ''

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
