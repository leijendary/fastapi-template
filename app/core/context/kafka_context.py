from aiokafka.producer.producer import AIOKafkaProducer
from app.core.configs.kafka_config import KafkaConfig


class KafkaProducerContext:
    instance: AIOKafkaProducer

    @classmethod
    async def init(cls, config: KafkaConfig):
        cls.instance = AIOKafkaProducer(
            client_id=config.client_id,
            bootstrap_servers=config.brokers,
            enable_idempotence=True
        )

        await cls.instance.start()

    @classmethod
    async def close(cls):
        await cls.instance.stop()

    @classmethod
    async def health(cls):
        try:
            version = await cls.instance.client.check_version()

            return "UP" if version else "DOWN"
        except:
            return "DOWN"
