import redis
import os
from app.config import logger

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

try:
    redis_client = redis.from_url(redis_url)
    redis_client.ping()
    logger.info("Connected to Redis successfully.")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None

def get_cache(key: str):
    if not redis_client:
        return None
    data = redis_client.get(key)
    return data.decode("utf-8") if data else None

def set_cache(key: str, value: str, ex: int = 3600):
    if not redis_client:
        return
    redis_client.set(key, value, ex=ex)