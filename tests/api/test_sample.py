from uuid import uuid4

import pytest
from app.configs.app_config import app_config
from app.core.logs.logging import get_logger
from fastapi.testclient import TestClient

_config = app_config()
logger = get_logger(__name__)


@pytest.mark.asyncio
def test_sample_create(client: TestClient):
    generated = uuid4()
    token = ""
    json = {
        "field_1": f"Test {generated}",
        "field_2": 1,
        "translations": [
            {
                "name": "Test",
                "description": "test description",
                "language": "en",
                "ordinal": 1
            },
            {
                "name": "Test japanese",
                "description": "testuuuu this is japanesuuu!!",
                "language": "jp",
                "ordinal": 2
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post(
        f"{_config.prefix}/api/v1/samples/",
        json=json,
        headers=headers
    )

    assert response.status_code == 201
