from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, roles_required
from app.db.models.user import RoleEnum, User
from app.schemas.color import ColorResponse, CreateColorDto, UpdateColorDto
from app.crud.crud_color import crud_color

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=ColorResponse)
@response_message("Created")
async def create_category(
    color: CreateColorDto,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    existed = await crud_color.get_one(db, {"name": color.name})
    if existed:
        raise HTTPException(status_code=409, detail="Color name existed")

    return await crud_color.create(db, color)


@router.get("", response_model=List[ColorResponse])
async def get_list(db: AsyncSessionDep):
    return await crud_color.get_list(db)


@router.get("/{id}", response_model=ColorResponse)
async def get_one(db: AsyncSessionDep, id: int):
    return await crud_color.get_one(db, {"id": id})


@router.put("/{id}", response_model=ColorResponse)
@response_message("Updated")
async def update(
    color: UpdateColorDto,
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    return await crud_color.update(db, id, color)


@router.delete("/{id}")
@response_message("Deleted")
async def delete(
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    return await crud_color.delete(db, id)
