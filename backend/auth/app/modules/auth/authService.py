from app.db.models.user import User
from sqlalchemy.orm import Session
from ...schemas.auth import LoginDto, SignUpDto
from ..user.userService import UserService
from ...core.baseService import BaseService
from ...utils.hashPass import HashHelper
from ...core.security import sign_jwt
from fastapi import HTTPException, status


class AuthService(BaseService):
    def __init__(self, session: Session) -> None:
        self.user_service = UserService(session=session)

    def register(self, data: SignUpDto):
        # Check email
        existing = self.user_service.get_one({"email": data.email})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

        # Hash password
        hashed_pw = HashHelper.get_password_hash(data.password)
        data.password = hashed_pw

        return self.user_service.create(data)

    def login(self, data: LoginDto):
        user = self.user_service.get_one({"email": data.email})

        if not user or not HashHelper.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid email or password",
            )

        # create token
        token = sign_jwt({"id": user.id})
        return {"token": token}
