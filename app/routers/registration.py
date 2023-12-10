from fastapi import APIRouter, HTTPException, status, Depends

from app.models import User
from app.schemas.user import CreateUser, ReturnUser
from app.users.exception import RegistrationException
from app.users.repository import UserRepository
from app.users.service import RegistrationService
from app.utils.exceptions import AlreadyExist
from app.utils.generic_repo import get_repository

router = APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post("/registration", response_model=ReturnUser,
             status_code=status.HTTP_201_CREATED)
async def register(creds: CreateUser,
                   repo=Depends(get_repository(model=User,
                                               repo=UserRepository))):
    try:
        service = RegistrationService(creds=creds, repo=repo)
        user = await service.register_user()
        return user
    except AlreadyExist as ae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exist") from ae

    except RegistrationException as reg_e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Service's not available") from reg_e

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"{e.__dict__}")