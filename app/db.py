from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.database_username}:' \
                          f'{settings.database_password}@' \
                          f'{settings.database_hostname}:' \
                          f'{settings.database_port}/' \
                          f'{settings.database_name}'


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()
