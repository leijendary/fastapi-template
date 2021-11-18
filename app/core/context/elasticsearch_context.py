from typing import Dict

from app.configs.elasticsearch_config import ElasticsearchConfig
from elasticsearch import AsyncElasticsearch


class ElasticsearchContext:
    instance: AsyncElasticsearch
    indices: Dict

    @classmethod
    def init(self, config: ElasticsearchConfig):
        self.instance = AsyncElasticsearch(
            hosts=config.hosts.split(','),
            use_ssl=config.use_ssl,
            verify_certs=config.verify_certs,
            ca_certs=config.ca_certs,
            client_cert=config.client_cert,
            client_key=config.client_key
        )

    @classmethod
    async def close(self):
        await self.instance.close()

    @classmethod
    async def init_indices(self, indices: Dict):
        client = self.instance.indices

        for index, body in indices.items():
            if await client.exists(index):
                await client.put_mapping(body['mappings'], index)
            else:
                await client.create(index, body)