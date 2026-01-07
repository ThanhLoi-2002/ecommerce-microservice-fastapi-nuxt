from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,  # 👈 bật log SQL
    pool_pre_ping=True,
    pool_recycle=3600,  # 1h
    execution_options={"prepared_statement_cache_size": 0},
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:  # Sử dụng context manager để bắt đầu transaction
        await conn.run_sync(Base.metadata.create_all)
