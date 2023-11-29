from sqlalchemy import select

from app.core.db import async_session_factory
from app.utils.generic_repo import GenericRepository


class UserRepository(GenericRepository):

    async def find_one_by_email(self, email: str):
        query = select(self.model).where(self.model.email == email)
        res = await self.session.execute(query)
        return res.scalar()
