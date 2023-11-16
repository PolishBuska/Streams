from app.auth.validator import AuthCredValidator
from app.auth.jwt_handler import AuthProvider
from app.auth.exceptions import WrongCredsException, AuthServiceError


class LoginService:
    validator = AuthCredValidator()
    jwt = AuthProvider()

    def __init__(self, email, plain_password):
        self.email = email
        self.plain_password = plain_password

    async def login(self):
        """getting tokens"""
        try:

            data = await self.validator.validate(email=self.email,
                                                 plain_password=self.plain_password)
            if not data:
                raise WrongCredsException from WrongCredsException
            access_token = await self.jwt.create_access_token(data=data)

            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        except Exception as er:
            raise AuthServiceError from er
