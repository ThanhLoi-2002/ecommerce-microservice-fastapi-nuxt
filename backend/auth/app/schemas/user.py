from pydantic import BaseModel, EmailStr, Field

from app.db.models.user import RoleEnum
from app.schemas.type import Image


class CreateUserDto(BaseModel):
    name: str = Field(..., min_length=2)  # ... = required
    email: EmailStr
    password: str = Field(..., min_length=6)


class UpdateUserDto(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    avatar: Image | None = None
    role: RoleEnum

    class Config:
        from_attributes = True  # Pydantic v2
