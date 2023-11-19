from sqlalchemy import select

from app.db import async_session_factory
from app.utils.generic_repo import GenericRepository


class UserRepository(GenericRepository):

    async def find_one_by_email(self, email: str):
        async with async_session_factory() as session:
            query = select(self.model).where(self.model.email == email)
            res = await session.execute(query)
            return res.scalar()
