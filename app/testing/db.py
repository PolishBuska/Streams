
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings
from app.main import app
from app.core.db import Base, get_session

engine = create_async_engine(url=settings.test_db_url)

test_session_factory = async_sessionmaker(
    engine, expire_on_commit=False
)

base: DeclarativeBase = Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def testing_get_session():
    async with test_session_factory() as session:
        yield session


app.dependency_overrides[get_session] = testing_get_session

