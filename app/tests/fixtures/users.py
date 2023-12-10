import pytest_asyncio
from fastapi import requests
from sqlalchemy import insert

from app.models import Roles


@pytest_asyncio.fixture(autouse=True, name="test_role")
async def test_role(async_session):
    stmt = insert(Roles).values(role="test", id=1).returning(Roles.id)
    await async_session.execute(stmt)
    await async_session.commit()
    print("added role ")


@pytest_asyncio.fixture(name="test_users")
async def test_users(client):

    user_data = [
        {
            'email': 'test2@gmail.com',
            'nickname': 'test2',
            'password': 'test2',
            'role_id': 1},
        {
            'email': 'test1@gmail.com',
            'nickname': 'test1',
            'password': 'test1',
            'role_id': 1
                                 }
                 ]
    for user in user_data:
        res = await client.post("/user/registration", json=user)
        print(f"Created user {res.json()}")
