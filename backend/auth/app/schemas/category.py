from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.db.models.category import GenderEnum
from app.schemas.type import BaseFilter, Image, PaginationParams


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    img: Optional[Image] = None
    description: Optional[str] = None
    pid: Optional[int] = None
    status: bool = True
    gender: GenderEnum


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    img: Optional[Image] = None
    description: Optional[str] = None
    pid: Optional[int] = None
    status: Optional[bool] = None
    gender: Optional[GenderEnum] = GenderEnum.MALE


class FilterCategories(PaginationParams, BaseFilter):
    name: Optional[str] = Field(None, max_length=255)
    pid: Optional[int] = None
    status: Optional[bool] = None
    parent_only: bool = False
    is_metadata: bool = False

    # method return attributes
    def get_attributes(self):
        page, limit = PaginationParams.get_attributes(self)
        sortBy, sortOrder = BaseFilter.get_attributes(self)
        return (
            self.name,
            self.pid,
            self.status,
            self.parent_only,
            page,
            limit,
            sortBy,
            sortOrder,
            self.is_metadata,
        )


class CategoryResponse(BaseModel):
    id: int
    slug: str
    name: str
    img: Optional[Image] = None
    pid: Optional[int] = None
    description: Optional[str] = None
    status: bool
    gender: GenderEnum
    created_at: datetime
    updated_at: datetime
    children_count: Optional[int] = 0
    children_count: int = 0

    class Config:
        from_attributes = True


class CategoryFullResponse(CategoryResponse):
    parent: Optional[CategoryResponse] = None
    children: Optional[List[CategoryResponse]] = []

    class Config:
        from_attributes = True
