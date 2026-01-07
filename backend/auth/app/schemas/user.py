from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.db.models.user import RoleEnum
from app.schemas.type import BaseFilter, Image, PaginationParams


class CreateUserDto(BaseModel):
    name: str = Field(..., min_length=2)  # ... = required
    email: EmailStr
    password: str = Field(..., min_length=6)


class UpdateUserDto(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr


class FilterUsers(PaginationParams, BaseFilter):
    email: Optional[str] = Field(None, max_length=255)
    is_metadata: bool = False

    # method return attributes
    def get_attributes(self):
        page, limit = PaginationParams.get_attributes(self)
        sortBy, sortOrder = BaseFilter.get_attributes(self)
        return (
            self.email,
            page,
            limit,
            sortBy,
            sortOrder,
            self.is_metadata,
        )


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    avatar: Image | None = None
    role: RoleEnum

    class Config:
        from_attributes = True  # Pydantic v2
