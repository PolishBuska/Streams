from sqlalchemy import select

from app.db import async_session_factory
from app.utils.generic_repo import GenericRepository


class SongRepository(GenericRepository):

    async def get_songs(self,
                        limit: int,
                        offset: int,
                        search: str):
        async with async_session_factory() as session:
            query = select(self.model).filter(
                self.model.title.contains(search)).limit(
                limit).offset(offset)
            res = await session.execute(query)
            return res.scalars().all()

    async def get_songs_by_user(self,
                                limit: int,
                                offset: int,
                                search: str,
                                user_id):
        async with async_session_factory() as session:
            query = (select(self.model).
                     where(self.model.author_id == user_id).
                     filter(
                self.model.title.contains(search)).
                     limit(
                limit).
                     offset(offset)
                     )
            res = await session.execute(query)
            return res.unique().scalars().all()
