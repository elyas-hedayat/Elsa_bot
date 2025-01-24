import redis

from .config import Config

redis_client = redis.Redis(host=Config.REDIS_HOST,
                           password=Config.REDIS_PASSWORD, port=Config.REDIS_PORT, db=0)
