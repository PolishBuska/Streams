from app.models import User
from app.schemas.user import CreateUser
from app.users.repository import UserRepository
from app.users.exception import RegistrationException
from app.utils.pwd import PwdContext


class RegistrationService:

    def __init__(self, creds: CreateUser):
        self.creds = creds
        self.repo = UserRepository(model=User)
        self.hasher = PwdContext()

    async def register_user(self):
        try:
            self.creds.password = self.hasher.pwd_context.hash(self.creds.password)
            user = await self.repo.add_one(data=self.creds.model_dump())
            return user
        except Exception as e:
            raise RegistrationException from e
