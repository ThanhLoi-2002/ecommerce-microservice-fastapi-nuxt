from fastapi import APIRouter
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.api.v1.deps import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.get("/me", response_model=UserResponse)
def me(user: CurrentUser):
    return user
