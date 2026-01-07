from typing import List, Optional
from sqlalchemy import case, desc, func, select, update
from app.db.models.user import User
from app.schemas.type import PaginatedResponse, SortOrder
from app.schemas.user import CreateUserDto, FilterUsers
from app.utils.hashPass import HashHelper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CRUDUser:
    @staticmethod
    async def get_one(db, filters: dict):
        q = select(User)

        for field, value in filters.items():
            if hasattr(User, field):
                q = q.where(getattr(User, field) == value)

        res = await db.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db, data: CreateUserDto):
        user = User(
            **data.model_dump(exclude={"password"}),
            password=HashHelper.get_password_hash(data.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def update(db, user: User, data: dict):
        for field, value in data.items():
            if hasattr(User, field):
                setattr(user, field, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_by_id(db, user_id: int, data: dict):
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )

        result = await db.execute(stmt)
        await db.commit()

        return result.fetchone()

    @staticmethod
    async def get_list(
        db: AsyncSession,
        query: FilterUsers,
        load_relations: Optional[List[str]] = None,
    ):
        (
            email,
            page,
            limit,
            sortBy,
            sortOrder,
            is_metadata,
        ) = query.get_attributes()

        # === BASE SELECT ===
        stmt = select(User)

        # === FILTERS ===
        if email:
            stmt = stmt.where(User.email.ilike(f"{email}%"))

        # === RELATIONS ===
        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(User, rel)))

        # === COUNT TOTAL ===
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(total_stmt)

        # === SORT ===
        if sortBy:
            col = getattr(User, sortBy)
            col = desc(col) if sortOrder == SortOrder.DESC else col.asc()
            stmt = stmt.order_by(col)
        else:
            stmt = stmt.order_by(User.id.desc())

        # === PAGINATION ===
        skip = (page - 1) * limit
        stmt = stmt.offset(skip).limit(limit)

        # === EXECUTE MAIN QUERY ===
        result = await db.execute(stmt)
        items = result.scalars().all()

        total_pages = (total + limit - 1) // limit

        # query metadata
        metadata = None

        if is_metadata:
            meta_stmt = select(
                func.count(User.id).label("total"),
                func.sum(case((User.status == True, 1), else_=0)).label(
                    "activeCount"
                ),
                func.sum(case((User.pid.is_(None), 1), else_=0)).label(
                    "parentCount"
                ),
                func.sum(case((User.pid.is_not(None), 1), else_=0)).label(
                    "childrenCount"
                ),
            )

            meta_result = await db.execute(meta_stmt)
            row = meta_result.one()

            metadata = {
                "activeCount": row.activeCount or 0,
                "parentCount": row.parentCount or 0,
                "childrenCount": row.childrenCount or 0,
            }

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            metadata=metadata,
        )

crud_user = CRUDUser()
