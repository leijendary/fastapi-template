from aiokafka.producer.producer import AIOKafkaProducer
from app.configs.kafka_config import KafkaConfig


class KafkaProducerContext:
    instance: AIOKafkaProducer

    @classmethod
    async def init(self, config: KafkaConfig):
        self.instance = AIOKafkaProducer(
            client_id=config.client_id,
            bootstrap_servers=config.brokers,
            enable_idempotence=True
        )

        await self.instance.start()

    @classmethod
    async def close(self):
        await self.instance.stop()
