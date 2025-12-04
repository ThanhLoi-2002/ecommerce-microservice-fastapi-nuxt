from app.modules.user.userModel import User
from sqlalchemy.orm import Session
from .dto.authValidatorDto import LoginDto, SignUpDto
from ..user.userService import UserService
from ...common.base.baseService import BaseService
from ...common.utils.hashPass import HashHelper
from ...common.utils.authHandler import AuthHandler
from fastapi import HTTPException, status


class AuthService(BaseService):
    def __init__(self, session: Session) -> None:
        self.user_service = UserService(session=session)

    def register(self, data: SignUpDto):
        # Check email tồn tại
        existing = self.user_service.get_one({"email": data.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

        # Hash password
        hashed_pw = HashHelper.get_password_hash(data.password)
        data.password = hashed_pw

        # Gọi create() từ BaseCRUD
        return self.user_service.create(data)

    # ---------------------
    # ĐĂNG NHẬP
    # ---------------------
    def login(self, data: LoginDto):
        user = self.user_service.get_one({"email": data.email})

        if not user or not HashHelper.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid email or password",
            )

        # Tạo token
        token = AuthHandler.sign_jwt({"user_id": user.id})
        return {"token": token}
