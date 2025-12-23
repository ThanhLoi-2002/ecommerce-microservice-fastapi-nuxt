from typing import Optional
from pydantic import BaseModel, Field


class CreateColorDto(BaseModel):
    name: str = Field(..., min_length=2)
    code: str = Field(..., min_length=2)


class UpdateColorDto(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class ColorResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True
