from app.core.auth.validator import AuthCredValidator
from app.core.auth.jwt_handler import AuthProvider
from app.core.auth.exceptions import WrongCredsException, AuthServiceError
from app.users.repository import UserRepository


class LoginService:
    validator = AuthCredValidator()
    jwt = AuthProvider()

    def __init__(self, email, plain_password, repo: UserRepository):
        self.email = email
        self.plain_password = plain_password
        self.repo = repo

    async def login(self):
        """getting tokens"""
        try:

            data = await self.validator.validate(
                                                 plain_password=self.plain_password,
                                                 db_user=await self.repo.find_one_by_email(email=self.email)
            )
            if not data:
                raise WrongCredsException from WrongCredsException
            access_token = await self.jwt.create_access_token(data=data)

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        except Exception as er:
            raise AuthServiceError from er
