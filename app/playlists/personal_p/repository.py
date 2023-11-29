from sqlalchemy import select, and_

from app.utils.exceptions import AlreadyExist
from app.playlists.exceptions import LikeAlreadyExist
from app.utils.generic_repo import GenericRepository
from app.models import Song, LikedSongs
from app.core.db import async_session_factory


class PersonalPlaylistRepository(GenericRepository):

    async def add_to_personal_playlist(self, data: dict):
        try:
            stmt = await self.add_one(data=data)
            return stmt
        except AlreadyExist as ae:
            raise LikeAlreadyExist from ae

    async def get_liked_songs_by_user(self, user_id, search, limit, offset):
        async with async_session_factory() as session:
            stmt = (
                select(Song).
                join(self.model, self.model.song_id == Song.id).
                where(
                    and_(
                        self.model.owner_id == user_id,
                        Song.title.contains(search)
                    )
                ).
                limit(limit).
                offset(offset)
            )
            result = await session.execute(stmt)
            return result.unique().scalars().all()



