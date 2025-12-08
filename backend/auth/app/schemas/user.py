from pydantic import BaseModel, EmailStr, Field

from app.db.models.user import RoleEnum


class CreateUserDto(BaseModel):
    name: str = Field(..., min_length=2)  # ... = required
    email: EmailStr
    password: str = Field(..., min_length=6)


class UpdateUserDto(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr


class Avatar(BaseModel):
    url: str
    public_id: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    avatar: Avatar | None = None
    role: RoleEnum

    class Config:
        from_attributes = True  # Pydantic v2
