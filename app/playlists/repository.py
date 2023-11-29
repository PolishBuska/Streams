from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.db import async_session_factory
from app.utils.generic_repo import GenericRepository
from app.models import PlaylistToSong


class PlaylistRepository(GenericRepository):
    async def get_playlist_with_songs(self, playlist_id: int):
            stmt = (
                select(self.model)
                .options(joinedload(PlaylistToSong.songs))
                .filter(PlaylistToSong.playlist_id == playlist_id)
            )

            result = await self.session.execute(stmt)
            playlist_to_songs = result.unique().scalars().all()

            if not playlist_to_songs:
                return None

            songs = [pts.songs for pts in playlist_to_songs]
            return songs

    async def find_one_pl(self,
                          limit: int,
                          offset: int,
                          search: str,
                          ):
            query = (select(self.model).
                     filter(
                self.model.title.contains(search)).
                     limit(
                limit).
                     offset(offset)
                     )
            res = await self.session.execute(query)
            return res.unique().scalars().all()
