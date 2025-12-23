from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.size import Size
from app.schemas.size import CreateSizeDto, UpdateSizeDto


class CRUDSize:
    @staticmethod
    async def get_one(
        db: AsyncSession,
        filters: dict,
        exclude_id: Optional[int] = None,
    ) -> Size | None:
        stmt = select(Size)
        for field, value in filters.items():
            if hasattr(Size, field) and value is not None:
                stmt = stmt.where(getattr(Size, field) == value)

        if exclude_id is not None:
            stmt = stmt.where(Size.id != exclude_id)

        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_list(
        db: AsyncSession
    ):
        # === BASE SELECT ===
        stmt = select(Size)

        # === EXECUTE MAIN QUERY ===
        result = await db.execute(stmt)
        items = result.scalars().all()

        return items

    @staticmethod
    async def create(db: AsyncSession, data: CreateSizeDto) -> Size:
        size = Size(**data.model_dump())
        db.add(size)
        await db.commit()
        await db.refresh(size)
        return size

    @staticmethod
    async def update(db: AsyncSession, id: int, data: UpdateSizeDto) -> Size | None:
        size = await CRUDSize.get_one(db, {"name": data.name}, id)

        if size:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Size name existed"
            )

        size = await CRUDSize.get_one(db, {"id": id})
        if not size:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(size, field, value)

        await db.commit()
        await db.refresh(size)
        return size

    @staticmethod
    async def delete(db: AsyncSession, id: int):
        stmt = delete(Size).where(Size.id == id)
        await db.execute(stmt)
        await db.commit()


crud_size = CRUDSize()
