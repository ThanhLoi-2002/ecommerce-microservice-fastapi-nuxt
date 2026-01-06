import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.common.decorator.responseMessage import response_message
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import AsyncSessionDep, roles_required
from app.db.models.user import RoleEnum, User
from app.socketio.server import sio

router = APIRouter(route_class=ResponseInterceptorRoute)


# @router.post("")
# async def send_message(
#     data: any,
#     db: AsyncSessionDep,
#     user: User = Depends(roles_required([RoleEnum.ADMIN, RoleEnum.USER])),
# ):
#     print(json.dumps(data))
#     await sio.emit("new_message", data, room=f"conversation_{data.conversation_id}")
#     return data
