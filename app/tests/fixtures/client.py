import pytest
from httpx import AsyncClient


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
