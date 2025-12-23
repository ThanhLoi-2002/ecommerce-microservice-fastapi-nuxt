from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, roles_required
from app.db.models.user import RoleEnum, User
from app.schemas.size import SizeResponse, CreateSizeDto, UpdateSizeDto
from app.crud.crud_size import crud_size

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("", response_model=SizeResponse)
@response_message("Created")
async def create_category(
    size: CreateSizeDto,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    existed = await crud_size.get_one(db, {"name": size.name})
    if existed:
        raise HTTPException(status_code=409, detail="Size name existed")

    return await crud_size.create(db, size)


@router.get("", response_model=List[SizeResponse])
async def get_list(db: AsyncSessionDep):
    return await crud_size.get_list(db)


@router.get("/{id}", response_model=SizeResponse)
async def get_category(db: AsyncSessionDep, id: int):
    return await crud_size.get_one(db, {"id": id})


@router.put("/{id}", response_model=SizeResponse)
@response_message("Updated")
async def update(
    size: UpdateSizeDto,
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    return await crud_size.update(db, id, size)


@router.delete("/{id}")
@response_message("Deleted")
async def delete(
    id: int,
    db: AsyncSessionDep,
    user: User = Depends(roles_required(RoleEnum.ADMIN)),
):
    return await crud_size.delete(db, id)
