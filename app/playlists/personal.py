from app.playlists.repository import PlaylistRepository


class PersonalPlaylist:

    def __init__(self, model):
        self.model = model
        self.repo = PlaylistRepository(model=self.model)

    async def add_to_personal_playlist(self, data: dict):
        stmt = await self.repo.add_one(data=data)
        return stmt
