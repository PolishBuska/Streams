"""this module provides with credentials' validator
free direct usage"""
from app.utils.pwd import PwdContext
from app.users.repository import UserRepository
from app.auth.exceptions import WrongCredsException, ValidatorError


class AuthCredValidator:
    """Do not expose user's password,"""

    _checker = PwdContext.pwd_context
    repo = UserRepository()

    async def validate(self, email: str, plain_password: str) -> dict:
        """Validate user's creds"""
        try:
            user = await self.repo.find_one_by_email(email=email)
            user_data = {"user_id": user.id, "role_id": user.role_id}
            if not self._checker.verify(plain_password, user.password):
                raise WrongCredsException from Exception
            return user_data
        except Exception as e:
            raise ValidatorError from e
