from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep
from app.schemas.category import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    FilterCategories,
)
from app.crud.crud_category import crud_category
from app.schemas.type import PaginatedResponse

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=CategoryResponse)
@response_message("Created category")
async def create_category(category: CategoryCreate, db: AsyncSessionDep):
    """Create a new category"""
    # Validate parent exists if pid is provided
    if category.pid:
        parent = await crud_category.get_one(db, {"id": category.pid})
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    return await crud_category.create(db, category)


@router.get("", response_model=PaginatedResponse[CategoryResponse])
async def get_categories(db: AsyncSessionDep, query: FilterCategories = Depends()):
    return await crud_category.get_categories(db, query, ['parent'])


@router.get("/{id}", response_model=CategoryResponse)
async def get_category(db: AsyncSessionDep, id: int):
    return await crud_category.get_one(db, {"id": id})


@router.put("/{id}", response_model=CategoryResponse)
@response_message("Updated category")
async def update_category(category: CategoryUpdate, db: AsyncSessionDep):
    # Validate parent exists if pid is provided
    if category.pid:
        parent = await crud_category.get_one(db, category.pid)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    return await crud_category.update(db, id, category)


@router.delete("/{id}", response_model=CategoryResponse)
@response_message("Deleted category")
async def update_category(id: int, db: AsyncSessionDep):
    return await crud_category.delete(db, id)
