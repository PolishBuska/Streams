from sqlalchemy import select
from sqlalchemy import insert

from app.db import async_session_maker
from app.models import Song


class SongRepository:
    model = Song

    async def add_one(self, data: dict) -> dict:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    async def find_all(self):
        async with async_session_maker() as session:
            query = select(self.model)
            res = await session.execute(query)
            return res.scalar()

    async def find_one(self, song_id: int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == song_id)
            res = await session.execute(query)
            return res.scalar()

    async def get_songs(self,
                        limit: int,
                        offset: int,
                        search: str):
        async with async_session_maker() as session:
            query = select(self.model).filter(
                self.model.title.contains(search)).limit(
                limit).offset(offset)
            res = await session.execute(query)
            return res.scalar()
