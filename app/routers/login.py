from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth.service import LoginService
from app.core.auth.exceptions import AuthServiceError

router = APIRouter(
    tags=['auth']
)


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    try:
        service = LoginService(plain_password=user_credentials.password, email=user_credentials.username)
        token = await service.login()
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Wrong credentials")
        return token
    except AuthServiceError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Currently not available")
