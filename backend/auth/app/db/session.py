from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

engine = create_async_engine(
    settings.POSTGRES_DB_URL,
    future=True,
    echo=True,# 👈 bật log SQL
    execution_options={"compiled_cache": {}},
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    print("create db")
    async with engine.begin() as conn:  # Sử dụng context manager để bắt đầu transaction
        await conn.run_sync(Base.metadata.create_all)
