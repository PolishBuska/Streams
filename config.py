from pydantic import ConfigDict, config
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_host: str
    app_port: int
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    static: str
    model_config = SettingsConfigDict(env_file='.env', extra="allow")

    @property
    def db_url(self):
        url = f'postgresql+asyncpg://{settings.database_username}:' \
                                  f'{settings.database_password}@' \
                                  f'{settings.database_hostname}:' \
                                  f'{settings.database_port}/' \
                                  f'{settings.database_name}'
        return url

    @property
    def test_db_url(self):
        url = f'postgresql+asyncpg://{settings.database_username}:' \
              f'{settings.database_password}@' \
              f'{settings.database_hostname}:' \
              f'{settings.database_port}/' \
              f'{settings.database_name}_test'
        return url


settings = Settings()
