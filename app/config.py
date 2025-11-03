import os
import logging
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Logger setup
logger = logging.getLogger("telex-cultural-coworker")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Redis client
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()
    logger.info("Connected to Redis successfully.")
except redis.exceptions.ConnectionError:
    logger.error("Failed to connect to Redis.")
    redis_client = None
