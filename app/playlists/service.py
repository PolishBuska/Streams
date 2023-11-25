from app.playlists.exceptions import PlaylistAlreadyExist, M2MRelationExists
from app.schemas.playlist import SongToPlaylist, CreatePlaylist
from app.utils.generic_repo import GenericRepository
from app.utils.exceptions import AlreadyExist, NotFound


class PlaylistService:
    def __init__(self, info: SongToPlaylist | CreatePlaylist,
                 repo: GenericRepository):
        if isinstance(info, CreatePlaylist):
            self._pl = info
        if isinstance(info, SongToPlaylist):
            self._s_pl = info
        self._repo = repo

    async def subscribe_s_to_p(self):
        try:
            result = await self._repo.add_one(data=self._s_pl.model_dump())
            return result
        except AlreadyExist as ae:
            raise M2MRelationExists from ae

    async def create_playlist(self, author_id):
        try:
            data = self._pl.model_dump()
            data["author_id"] = author_id
            pl = await self._repo.add_one(data=data)
            return pl
        except AlreadyExist as ae:
            raise PlaylistAlreadyExist from ae
        except Exception as e:
            raise e from e

    @staticmethod
    async def find_pl_related_songs(repo, pl_id: int):
        res = await repo.get_playlist_with_songs(playlist_id=pl_id)
        if not res:
            raise NotFound
        return res

