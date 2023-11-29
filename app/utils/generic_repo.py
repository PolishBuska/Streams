from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.exceptions import AlreadyExist
from app.core.db import get_session

from fastapi import Depends


class GenericRepository:
    def __init__(self, model, session):
        self.model = model
        self.session = session

    async def add_one(self, data: dict) -> dict | None:
        try:
            stmt = insert(self.model).values(data).returning(self.model)
            res = await self.session.execute(stmt)
            await self.session.commit()
            return res.scalar()
        except IntegrityError as ie:
            raise AlreadyExist from ie
        except Exception as e:
            raise e from e

    async def find_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        return res.scalars().unique().all()

    async def find_one(self, pk: int):
        query = select(self.model).where(self.model.id == pk)
        res = await self.session.execute(query)
        return res.scalar()


def get_repository(model, repo):
    def _get_generic_repository(session: AsyncSession = Depends(get_session)):
        return repo(model, session)

    return _get_generic_repository
