import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.testing.db import create_tables

client = TestClient(app=app)


@pytest.fixture(scope='module', autouse=True)
async def create_test_tables():
    yield create_tables()


def test_root():
    res = client.get('/')
    assert res.json() == "Hello world"
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_check_registration():
    res = client.post("/user/registration",
                      json={"email": "123@1.com",
                            "password": "123123",
                            "nickname": "lol",
                            "role_id": 1})
    assert res.status_code == 201
