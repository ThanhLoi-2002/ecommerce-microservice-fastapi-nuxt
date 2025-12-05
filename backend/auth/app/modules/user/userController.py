from fastapi import APIRouter, Depends, Request
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.core.db import get_db
from app.core.deps import CurrentUser
from .userService import UserService
from sqlalchemy.orm import Session
from ..user.dto.userResponse import UserResponse

userRouter = APIRouter(
    route_class=ResponseInterceptorRoute, tags=["user"], prefix="/user"
)


@userRouter.get("/me", response_model=UserResponse)
def me(user: CurrentUser, session: Session = Depends(get_db)):
    print(user)
    return UserService(session=session).get_one({"user_id": user.user_id})
