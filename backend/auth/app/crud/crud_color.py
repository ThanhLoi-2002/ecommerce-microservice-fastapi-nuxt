from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.color import Color
from app.schemas.color import CreateColorDto, UpdateColorDto


class CRUDColor:
    @staticmethod
    async def get_one(
        db: AsyncSession,
        filters: dict,
        exclude_id: Optional[int] = None,
    ) -> Color | None:
        q = select(Color)
        for field, value in filters.items():
            if hasattr(Color, field) and value is not None:
                q = q.where(getattr(Color, field) == value)

        if exclude_id is not None:
            q = q.where(Color.id != exclude_id)

        result = await db.execute(q)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_list(
        db: AsyncSession
    ):
        # === BASE SELECT ===
        q = select(Color)

        # === EXECUTE MAIN QUERY ===
        result = await db.execute(q)
        items = result.scalars().all()

        return items

    @staticmethod
    async def create(db: AsyncSession, data: CreateColorDto) -> Color:
        color = Color(**data.model_dump())
        db.add(color)
        await db.commit()
        await db.refresh(color)
        return color

    @staticmethod
    async def update(db: AsyncSession, id: int, data: UpdateColorDto) -> Color | None:
        color = await CRUDColor.get_one(db, {"name": data.name}, id)

        if color:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Color name existed"
            )

        color = await CRUDColor.get_one(db, {"id": id})
        if not color:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(color, field, value)

        await db.commit()
        await db.refresh(color)
        return color

    @staticmethod
    async def delete(db: AsyncSession, id: int):
        stmt = delete(Color).where(Color.id == id)
        await db.execute(stmt)
        await db.commit()


crud_color = CRUDColor()
