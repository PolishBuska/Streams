from sqlalchemy import select, insert

from app.db import async_session_factory
from app.utils.generic_repo import GenericRepository


class PlaylistRepository(GenericRepository):

    async def find_one_pl(self,
                          limit: int,
                          offset: int,
                          search: str,
                          ):
        async with async_session_factory() as session:
            query = (select(self.model).
                     filter(
                self.model.title.contains(search)).
                     limit(
                limit).
                     offset(offset)
                     )
            res = await session.execute(query)
            return res.scalars().all()
