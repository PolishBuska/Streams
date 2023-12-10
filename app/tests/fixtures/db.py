from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, SessionTransaction

from app.core.db import Base, get_session
from config import settings


@pytest.fixture(autouse=True)
def setup_test_db() -> Generator:
    engine = create_engine(str(settings.test_db_url).replace('+asyncpg', ''))

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield


@pytest_asyncio.fixture(autouse=True, name="async_session")
async def session(app) -> AsyncGenerator:
    async_engine = create_async_engine(str(settings.test_db_url))
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        async_session_factory = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            autoflush=True,
            bind=conn,
        )

        async_session = async_session_factory()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(_session: Session, _transaction: SessionTransaction) -> None:

            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        def test_get_session() -> Generator:
            try:
                yield async_session_factory()
            except SQLAlchemyError:
                pass

        app.dependency_overrides[get_session] = test_get_session

        await async_session.close()
        yield async_session


