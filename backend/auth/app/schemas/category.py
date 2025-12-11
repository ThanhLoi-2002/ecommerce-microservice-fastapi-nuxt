from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

from sqlalchemy import Tuple

from app.schemas.type import BaseFilter, Image, PaginationParams


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    img: Optional[Image] = None
    pid: Optional[int] = None
    status: bool = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    img: Optional[Image] = None
    pid: Optional[int] = None
    status: Optional[bool] = None


class FilterCategories(PaginationParams, BaseFilter):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    pid: Optional[int] = None
    status: Optional[bool] = None
    parent_only: bool = False

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
        )


class CategoryResponse(BaseModel):
    id: int
    slug: str
    name: str
    img: Image
    status: bool
    created_at: datetime
    updated_at: datetime
    children_count: Optional[int] = 0

    class Config:
        from_attributes = True


class CategoryTreeResponse(CategoryResponse):
    children: List["CategoryTreeResponse"] = []
