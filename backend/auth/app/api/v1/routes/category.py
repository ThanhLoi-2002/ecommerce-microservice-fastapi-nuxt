from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, roles_required
from app.db.models.user import RoleEnum, User
from app.schemas.category import (
    CategoryResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryFullResponse,
    FilterCategories,
)
from app.crud.crud_category import crud_category
from app.schemas.type import PaginatedResponse

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=CategoryResponse)
@response_message("Created category")
async def create_category(
    category: CategoryCreate,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    """Create a new category"""
    # Validate parent exists if pid is provided
    if category.pid:
        parent = await crud_category.get_one(db, {"id": category.pid})
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    return await crud_category.create(db, category)


@router.get("", response_model=PaginatedResponse[CategoryFullResponse])
async def get_categories(db: AsyncSessionDep, query: FilterCategories = Depends()):
    categories = await crud_category.get_categories(db, query, ["parent", "children"])
    return categories


@router.get("/{id}", response_model=CategoryResponse)
async def get_category(db: AsyncSessionDep, id: int):
    return await crud_category.get_one(db, {"id": id})


@router.put("/{id}", response_model=CategoryResponse)
@response_message("Updated category")
async def update_category(
    category: CategoryUpdate,
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    # Validate parent exists if pid is provided
    if category.pid:
        parent = await crud_category.get_one(db, {"id": category.pid})
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    return await crud_category.update(db, id, category)


@router.delete("/{id}")
@response_message("Deleted category")
async def update_category(
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    return await crud_category.delete(db, id)
