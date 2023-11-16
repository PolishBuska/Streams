from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from app.config import settings
from app.models import User
from app.schemas.jwt import TokenPayLoad
from app.users.repository import UserRepository


class AuthProvider:
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
    Model = User
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

    async def create_access_token(self,
                                  data: dict):
        if not isinstance(data, dict):
            raise ValueError("Invalid input data")
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt

    async def verify_access_token(self,
                                  token: str,
                                  credentials_exception):
        try:
            payload = jwt.decode(token,
                                 self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])
            user_id = payload.get("user_id")
            role_id = payload.get("role_id")

            token_data = TokenPayLoad(user_id=user_id,
                                      role_id=role_id)
        except JWTError:
            raise credentials_exception
        return token_data

    async def get_current_user(self,
                               token: str = Depends(oauth2_scheme)):
        try:
            credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail=f'Could not validate credentials',
                                                  headers={"WWW-Authenticate": "Bearer"})
            token_verified = await self.verify_access_token(token, credentials_exception)
            db_manager = UserRepository()
            user = await db_manager.find_one(user_id=token_verified.user_id)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f'Could not validate credentials',
                                headers={"WWW-Authenticate": "Bearer"})
        return user
