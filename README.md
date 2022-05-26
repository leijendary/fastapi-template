# FastAPI Template for Microservices

- This template is intended for the microservice architecture
- Kafka is included in this template
- Sample files are included
- **Intended for personal use only as this does not include complete features**

# Technologies Used:

- FastAPI
- Hypercorn[uvloop]
- Tortoise ORM
- Dotenv
- Aerich
- AIO Kafka
- Elasticsearch
- FastAPI Pagination
- Multipart
- JOSE
- HTTPX
- Redis
- Boto3 (AWS SDK)
- PyCryptodome
- PyTest
- Starlette Context
- Starlette Prometheus
- OpenTelemetry
    - Exporter - Jaeger
    - Propagator - B3
    - Instrumentation - asyncpg
    - Instrumentation - FastAPI
    - Instrumentation - HTTPX
    - Instrumentation - Redis

# FastAPI Microservice Template

### To run the code:

`python -m hypercorn main:app --config python:hypercorn_conf`
