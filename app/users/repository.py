from sqlalchemy import select
from sqlalchemy import insert

from app.db import async_session_maker
from app.models import User


class UserRepository:
    model = User

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

    async def find_one(self, user_id: int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == user_id)
            res = await session.execute(query)
            return res.scalar()
