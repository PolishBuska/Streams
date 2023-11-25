from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    static: str

    @property
    def db_url(self):
        url = f'postgresql+asyncpg://{settings.database_username}:' \
                                  f'{settings.database_password}@' \
                                  f'{settings.database_hostname}:' \
                                  f'{settings.database_port}/' \
                                  f'{settings.database_name}'
        return url

    class Config:
        env_file = ".env"
        extra = 'allow'


settings = Settings()
