from fastapi import APIRouter, Depends
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.common.decorator.responseMessage import response_message
from .authService import AuthService
from .dto.authValidatorDto import LoginDto, SignUpDto
from sqlalchemy.orm import Session
from ...common.database import get_db
from ..user.dto.userResponse import UserResponse

authRouter = APIRouter(
    route_class=ResponseInterceptorRoute, tags=["auth"], prefix="/auth"
)

@authRouter.post("/login")
@response_message("Logged in")
def login(loginData: LoginDto, session: Session = Depends(get_db)):
    return AuthService(session=session).login(loginData)


@authRouter.post("/signup", response_model=UserResponse)
@response_message("Sign up successfully")
def signup(signUpData: SignUpDto, session: Session = Depends(get_db)):
    return AuthService(session=session).register(signUpData)
