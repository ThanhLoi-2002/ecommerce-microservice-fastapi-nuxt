import json
from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, CurrentUser, roles_required
from app.db.models.user import RoleEnum, User
from app.schemas.type import Image, PaginatedResponse
from app.schemas.user import SearchUserDto, UpdateUserDto, UserResponse
from app.crud.crud_user import crud_user
from app.core.cloudinary_config import cloudinary
import cloudinary.uploader

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.get("/me", response_model=UserResponse)
def me(
    user: User = Depends(roles_required([RoleEnum.ADMIN, RoleEnum.USER])),
):
    return user


@router.get("/search-user", response_model=UserResponse)
async def searchUser(
    db: AsyncSessionDep,
    search: SearchUserDto = Depends(),
    _: User = Depends(roles_required([RoleEnum.ADMIN, RoleEnum.USER])),
):
    user = await crud_user.get_one(db, {"email": search.email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("", response_model=UserResponse)
@response_message("Updated profile")
async def updateProfile(user: CurrentUser, data: UpdateUserDto, db: AsyncSessionDep):
    newData = await crud_user.update(db, user, data.__dict__)
    return newData


@router.put("/update-avatar", response_model=UserResponse)
@response_message("Updated avatar")
async def updateAvatar(user: CurrentUser, avatar: Image, db: AsyncSessionDep):
    public_id = user.avatar.get("public_id") if user.avatar else None

    if public_id:
        cloudinary.uploader.destroy(public_id)
    newData = await crud_user.update(db, user, {"avatar": avatar.__dict__})
    return newData
