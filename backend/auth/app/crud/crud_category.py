from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, desc, func, select
from typing import Any, Dict, Optional, List
from app.db.models.category import Category
from app.schemas.category import CategoryResponse, FilterCategories
from app.schemas.type import PaginatedResponse, SortOrder
from app.schemas.category import CategoryCreate, CategoryUpdate
from slugify import slugify
from sqlalchemy.orm import selectinload


class CRUDCategory:
    @staticmethod
    async def generate_unique_slug(
        db: AsyncSession, name: str, id: Optional[int] = None
    ) -> str:
        """Generate unique slug for category"""
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        while True:
            category = await CRUDCategory.get_one(db, {"slug": slug}, None, id)

            if not category:
                return slug

            slug = f"{base_slug}-{counter}"
            counter += 1

    @staticmethod
    async def get_one(
        db: AsyncSession,
        filters: Dict[str, Any] = None,
        load_relations: Optional[List[str]] = None,
        exclude_id: Optional[int] = None,
    ):
        q = select(Category)

        if filters:
            conditions = []

            for field, value in filters.items():
                if hasattr(Category, field):
                    if isinstance(value, str):
                        conditions.append(getattr(Category, field).ilike(f"%{value}%"))
                    elif isinstance(value, list):  # Hỗ trợ tìm kiếm nhiều giá trị
                        conditions.append(getattr(Category, field).in_(value))
                    else:
                        conditions.append(getattr(Category, field) == value)
            q = q.where(and_(*conditions))

        if exclude_id is not None:
            q = q.where(Category.id != exclude_id)

        # Load relationships
        if load_relations:
            for relation in load_relations:
                if hasattr(Category, relation):
                    query = query.options(selectinload(getattr(Category, relation)))

        res = await db.execute(q)
        return res.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: CategoryCreate) -> Category:
        """Create new category"""
        slug = await CRUDCategory.generate_unique_slug(db, data.name)

        category = Category(
            **data.model_dump(exclude={"slug"}),
            slug=slug,
        )

        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_categories(
        db: AsyncSession,
        query: FilterCategories,
        load_relations: Optional[List[str]] = None,
    ) -> PaginatedResponse[CategoryResponse]:

        (
            name,
            pid,
            status,
            parent_only,
            page,
            limit,
            sortBy,
            sortOrder,
        ) = query.get_attributes()

        # === BASE SELECT ===
        stmt = select(Category)

        # === FILTERS ===
        if name:
            stmt = stmt.where(Category.name.ilike(f"%{name}%"))

        if status is not None:
            stmt = stmt.where(Category.status == status)

        if parent_only:
            stmt = stmt.where(Category.pid.is_(None))
        elif pid is not None:
            stmt = stmt.where(Category.pid == pid)

        # === RELATIONS ===
        if load_relations:
            for rel in load_relations:
                stmt = stmt.options(selectinload(getattr(Category, rel)))

        # === COUNT TOTAL ===
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = await db.scalar(total_stmt)

        # === SORT ===
        if sortBy:
            col = getattr(Category, sortBy)
            col = desc(col) if sortOrder == SortOrder.DESC else col.asc()
            stmt = stmt.order_by(col)
        else:
            stmt = stmt.order_by(Category.id.desc())

        # === PAGINATION ===
        skip = (page - 1) * limit
        stmt = stmt.offset(skip).limit(limit)

        # === EXECUTE MAIN QUERY ===
        result = await db.execute(stmt)
        items = result.scalars().all()

        # === CHILDREN COUNT ===
        for item in items:
            count_stmt = select(func.count(Category.id)).where(Category.pid == item.id)
            item.children_count = await db.scalar(count_stmt)

        total_pages = (total + limit - 1) // limit

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )

    # @staticmethod
    # def CRUDCategory.get_one_tree(db: AsyncSession) -> List[Category]:
    #     """Get category tree structure (parent with children)"""

    #     def build_tree(parent_id: Optional[int] = None) -> List[Category]:
    #         categories = db.query(Category).filter(Category.pid == parent_id).all()
    #         for category in categories:
    #             category.children = build_tree(category.id)
    #             category.children_count = len(category.children)
    #         return categories

    #     return build_tree()

    @staticmethod
    async def update(
        db: AsyncSession, id: int, category_update: CategoryUpdate
    ) -> Optional[Category]:
        """Update category"""
        category = await CRUDCategory.get_one(db, id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        update_data = category_update.model_dump(exclude_unset=True)

        # Update slug if name changed
        if "name" in update_data:
            update_data["slug"] = await CRUDCategory.generate_unique_slug(
                db, update_data["name"], id
            )

        for field, value in update_data.items():
            setattr(category, field, value)

        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete(db: AsyncSession, id: int) -> bool:
        """Delete category (soft delete by setting status to False)"""
        category = await CRUDCategory.get_one(db, id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        # Check if category has children
        children_count = await (
            db.query(func.count(Category.id)).filter(Category.pid == id).scalar()
        )
        if children_count > 0:
            raise ValueError("Cannot delete category with children")

        await db.delete(category)
        await db.commit()
        return True


crud_category = CRUDCategory()
