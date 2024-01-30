# from dotenv import dotenv_values
import contextlib
from app.config.settings import settings
from typing import Any, AsyncIterator
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

Base: DeclarativeMeta = declarative_base()

# config = dotenv_values('.env')
# db_host = config["DATABASE_URL"]
# db_name = config["DATABASE_NAME"]
# db_user = config["DATABASE_USER"]
# db_password = config["DATABASE_PASSWORD"]


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


url = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    username=settings.database_user,
    password=settings.database_user,
    host=settings.database_url,
    path=settings.database_name
).unicode_string()

sessionmanager = DatabaseSessionManager(
    url,
    {"echo": settings.echo_sql}
)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


# url = PostgresDsn.build(
#     scheme="postgresql+asyncpg",
#     username=db_user,
#     password=db_password,
#     host=db_host,
#     path=db_name
# ).unicode_string()
# engine = create_async_engine(
#     url,
#     pool_pre_ping=True,
#     echo=True,
# )
# SessionLocal = async_sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )
# Base: DeclarativeMeta = declarative_base()


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def create_tables():
#     Base.metadata.create_all(bind=engine)
