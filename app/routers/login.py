from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth.service import LoginService
from app.core.auth.exceptions import AuthServiceError
from app.models import User
from app.users.repository import UserRepository
from app.utils.generic_repo import get_repository

router = APIRouter(
    tags=['auth']
)


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
                repo=Depends(get_repository(model=User,
                                            repo=UserRepository))):
    try:
        if not user_credentials:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided")
        service = LoginService(plain_password=user_credentials.password,
                               email=user_credentials.username,
                               repo=repo)
        token = await service.login()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Wrong credentials")
        return token
    except AuthServiceError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Currently not available")
