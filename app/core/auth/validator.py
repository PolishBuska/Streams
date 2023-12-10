"""this module provides with credentials' validator
free direct usage"""
from app.utils.pwd import PwdContext
from app.users.repository import UserRepository
from app.core.auth.exceptions import WrongCredsException, ValidatorError
from app.models import User


class AuthCredValidator:
    """Do not expose user's password,"""

    _checker = PwdContext.pwd_context

    async def validate(self, plain_password: str, db_user: User) -> dict:
        """Validate user's creds"""
        try:
            if db_user and plain_password:
                user_data = {"user_id": db_user.id, "role_id": db_user.role_id}

                if not self._checker.verify(plain_password, db_user.password):
                    raise WrongCredsException(user_data) from Exception
                return user_data
        except Exception as e:
            raise ValidatorError from e
