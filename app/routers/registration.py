from fastapi import APIRouter, HTTPException, status

from app.schemas.user import CreateUser, ReturnUser
from app.users.service import RegistrationService
from app.users.exception import RegistrationException
from app.utils.exceptions import AlreadyExist

router = APIRouter(
    prefix="/user",
    tags=['users']
)


@router.post("/registration", response_model=ReturnUser,
             status_code=status.HTTP_201_CREATED)
async def register(creds: CreateUser):
    try:
        service = RegistrationService(creds=creds)
        user = await service.register_user()
        return user
    except AlreadyExist as ae:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exist") from ae

    except RegistrationException as reg_e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Service's not available") from reg_e

