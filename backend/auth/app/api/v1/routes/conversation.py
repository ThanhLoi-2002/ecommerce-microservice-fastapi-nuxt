from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, roles_required
from app.db.models.user import RoleEnum, User

router = APIRouter(route_class=ResponseInterceptorRoute)


# @router.post("",)
# @response_message("Created")
# async def create_category(
#     db: AsyncSessionDep,
#     user: User = Depends(roles_required([RoleEnum.ADMIN, RoleEnum.USER])),
# ):
#     pass