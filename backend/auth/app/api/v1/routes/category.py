from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep
from app.schemas.category import CategoryResponse, CategoryCreate, FilterCategories
from app.crud.crud_category import crud_category
from app.schemas.type import PaginatedResponse

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=CategoryResponse)
@response_message("Created category")
async def create_category(category: CategoryCreate, db: AsyncSessionDep):
    """Create a new category"""
    # Validate parent exists if pid is provided
    if category.pid:
        parent = await crud_category.get_one(db, category.pid)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    return await crud_category.create_category(db, category)


@router.get("", response_model=PaginatedResponse[CategoryResponse])
async def get_categories(db: AsyncSessionDep, query: FilterCategories = Depends()):
    return await crud_category.get_categories(db, query)
