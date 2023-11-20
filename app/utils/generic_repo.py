from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from app.db import async_session_factory
from app.utils.exceptions import AlreadyExist


class GenericRepository:
    def __init__(self, model):
        self.model = model

    async def add_one(self, data: dict) -> dict | None:
        async with async_session_factory() as session:
            try:
                stmt = insert(self.model).values(data).returning(self.model)
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar()
            except IntegrityError as ie:
                raise AlreadyExist from ie
            except Exception as e:
                raise e from e

    async def find_all(self):
        async with async_session_factory() as session:
            query = select(self.model)
            res = await session.execute(query)
            return res.scalars().all()

    async def find_one(self, pk: int):
        async with async_session_factory() as session:
            query = select(self.model).where(self.model.id == pk)
            res = await session.execute(query)
            return res.scalar()
