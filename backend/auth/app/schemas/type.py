from fastapi import Query
from pydantic import BaseModel
from typing import Generic, Optional, TypeVar, List
from enum import Enum


class SortOrder(str, Enum):
    ASC = "ASC"   # Sắp xếp tăng dần
    DESC = "DESC"  # Sắp xếp giảm dần


T = TypeVar("T")


class Image(BaseModel):
    url: str
    public_id: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1, le=100)

    def get_attributes(self):
        return self.page, self.limit


class BaseFilter(BaseModel):
    sortBy: Optional[str] = None
    sortOrder: Optional[SortOrder] = SortOrder.ASC

    def get_attributes(self):
        return self.sortBy, self.sortOrder
