from typing import Optional
from pydantic import BaseModel, Field


class CreateConversation(BaseModel):
    name: str = Field(..., min_length=2)
    code: str = Field(..., min_length=2)


class UpdateConversation(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True
