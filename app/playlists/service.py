from app.playlists.exceptions import PlaylistAlreadyExist
from app.schemas.playlist import SongToPlaylist, CreatePlaylist
from app.utils.generic_repo import GenericRepository
from app.utils.exceptions import AlreadyExist


class PlaylistService:
    def __init__(self, info: SongToPlaylist | CreatePlaylist,
                 repo: GenericRepository):
        if isinstance(info, CreatePlaylist):
            self.pl = info
        if isinstance(info, SongToPlaylist):
            self.s_pl = info
        self.repo = repo

    async def subscribe_s_to_p(self):
        result = await self.repo.add_one(data=self.s_pl.model_dump())
        return result

    async def create_playlist(self, author_id):
        try:
            data = self.pl.model_dump()
            data["author_id"] = author_id
            pl = await self.repo.add_one(data=data)
            return pl
        except AlreadyExist as ae:
            raise PlaylistAlreadyExist from ae
        except Exception as e:
            raise e from e
