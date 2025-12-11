from fastapi import APIRouter
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, CurrentUser
from app.schemas.type import Image
from app.schemas.user import UpdateUserDto, UserResponse
from app.crud.crud_user import crud_user

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.get("/me", response_model=UserResponse)
def me(user: CurrentUser):
    return user


@router.put("", response_model=UserResponse)
@response_message("Updated profile")
async def updateProfile(user: CurrentUser, data: UpdateUserDto, db: AsyncSessionDep):
    newData = await crud_user.update(db, user, data.__dict__)
    return newData


@router.put("/update-avatar", response_model=UserResponse)
@response_message("Updated avatar")
async def updateAvatar(user: CurrentUser, avatar: Image, db: AsyncSessionDep):
    newData = await crud_user.update(
        db, user, {"avatar": avatar.__dict__}
    )
    return newData
