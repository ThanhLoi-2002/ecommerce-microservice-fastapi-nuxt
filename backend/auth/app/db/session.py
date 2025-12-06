from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(settings.POSTGRES_DB_URL, echo=True, query_cache_size=0)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:  # Sử dụng context manager để bắt đầu transaction
        await conn.run_sync(Base.metadata.create_all)
