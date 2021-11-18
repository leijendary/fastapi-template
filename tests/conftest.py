import asyncio
from asyncio.events import AbstractEventLoop
from typing import Generator

import pytest
from app.core.databases.tortoise_orm import MODULE, MODULES
from fastapi.testclient import TestClient
from main import app
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope='session', autouse=True)
def client(event_loop: AbstractEventLoop) -> Generator:
    register_tortoise(
        app,
        db_url='sqlite://:memory:',
        modules=MODULES,
        generate_schemas=True
    )

    initializer([MODULE], loop=event_loop)

    with TestClient(app) as client:
        yield client

    finalizer()


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop

    loop.close()
