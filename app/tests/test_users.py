import urllib.parse

import pytest


@pytest.mark.parametrize("user_credentials", [
    ({"username": "test1@gmail.com", "password": "test1"}),
    ({"username": "test2@gmail.com", "password": "test2"}),
])
async def test_login(test_users, client, user_credentials):

    form_data = urllib.parse.urlencode(user_credentials)
    res = await client.post("/login",
                            content=form_data,
                            headers={"Content-type": "application/x-www-form-urlencoded"})

    assert "access_token" in res.json()
