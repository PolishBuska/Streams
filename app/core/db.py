from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings


engine = create_async_engine(url=settings.db_url)

async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False
)
Base = declarative_base()


async def get_session():
    async with async_session_factory() as session:
        yield session
