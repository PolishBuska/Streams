import io

import pytest


@pytest.mark.parametrize("test_songs", [
    {"title": "test_song1", "description": "desc1", }
])
async def test_song(authorized_client, test_songs):
    fake_file = io.BytesIO(b"fake mp3 data")
    fake_file.name = "test_song.mp3"

    response = await authorized_client.post(
        "/publisher/create",
        params=test_songs,
        files={"file": fake_file},
    )

    assert response.status_code == 200
    print(response.json())




