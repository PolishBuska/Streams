from fastapi import HTTPException
from sqlalchemy import select
from starlette import status
from passlib.context import CryptContext

from app.db import async_session_maker
from app.models import User
from app.users.repository import UserRepository


class AuthCredValidator(UserRepository):
    pwd_context = CryptContext(schemes=['bcrypt'],
                               deprecated='auto')
    model = User

    async def validate(self, email: str, plain_password: str):
        async with async_session_maker() as session:
            query_user = select(self.model).where(self.model.email == email)
            res = await session.execute(query_user)
            res_out = res.scalar()
            if not self.pwd_context.verify(plain_password, res_out.password):
                raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Wrong credentials")
            return res_out
