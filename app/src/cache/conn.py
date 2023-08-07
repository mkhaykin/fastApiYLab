import aioredis
from aioredis.client import Redis

from app.src.config import settings

REDIS_URL: str = f'redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}'
client: Redis = aioredis.from_url(REDIS_URL)
