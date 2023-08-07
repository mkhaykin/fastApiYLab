import aioredis

from app.src.config import settings

REDIS_URL = f'redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}'
client = aioredis.from_url(REDIS_URL)
