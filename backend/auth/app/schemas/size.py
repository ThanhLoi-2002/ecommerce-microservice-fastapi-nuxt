from typing import Optional
from pydantic import BaseModel, Field


class CreateSizeDto(BaseModel):
    name: str = Field(...)


class UpdateSizeDto(BaseModel):
    name: Optional[str] = None


class SizeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
