from fastapi import APIRouter, Depends
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.common.decorator.responseMessage import response_message
from app.core.deps import get_db, CurrentUser
from .authService import AuthService
from .dto.authValidatorDto import LoginDto, SignUpDto
from sqlalchemy.orm import Session
from ..user.dto.userResponse import UserResponse

authRouter = APIRouter(
    route_class=ResponseInterceptorRoute, tags=["auth"], prefix="/auth"
)

@authRouter.get("/test/")
async def read_items(api_key: CurrentUser):
    return [{"item": "item1"}, {"item": "item2"}]

@authRouter.post("/login")
@response_message("Logged in")
async def login(form_data: LoginDto, session: Session = Depends(get_db)):
    return AuthService(session=session).login(form_data)


@authRouter.post("/signup", response_model=UserResponse)
@response_message("Sign up successfully")
def signup(signUpData: SignUpDto, session: Session = Depends(get_db)):
    return AuthService(session=session).register(signUpData)
