from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.settings import settings_db

sqlalchemy_database_uri = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user=settings_db.DB_USER,
    password=settings_db.DB_PASSWORD,
    host=settings_db.DB_HOST,
    port=settings_db.DB_PORT,
    path=f"/{settings_db.DB_NAME or ''}",
)

engine = create_async_engine(sqlalchemy_database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
