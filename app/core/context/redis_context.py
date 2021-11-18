from aioredis.client import Redis
from aioredis.utils import from_url
from app.configs.cache_config import CacheConfig


class RedisContext:
    instance: Redis

    @classmethod
    def init(self, config: CacheConfig):
        scheme = 'rediss' if config.use_ssl else 'redis'

        self.instance = from_url(
            f"{scheme}://{config.redis_host}:{config.redis_port}",
            username=config.username,
            password=config.password,
            decode_responses=True
        )

    @classmethod
    async def close(self):
        await self.instance.close()
