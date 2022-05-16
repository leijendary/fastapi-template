import asyncio
from asyncio.events import AbstractEventLoop
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer

from app.core.databases.main_sql import _module, _modules
from main import app


@pytest.fixture(scope="session", autouse=True)
def client(event_loop: AbstractEventLoop) -> Generator:
    register_tortoise(
        app,
        db_url="sqlite://:memory:",
        modules=_modules,
        generate_schemas=True
    )

    initializer([_module], loop=event_loop)

    with TestClient(app) as client:
        yield client

    finalizer()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop

    loop.close()
