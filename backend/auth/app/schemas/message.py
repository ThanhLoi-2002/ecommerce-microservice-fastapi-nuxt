from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime
from app.db.models.message import MessageType
from app.schemas.user import UserResponse


class CreateMessage(BaseModel):
    conversation_id: int
    content: str
    type: MessageType = MessageType.TEXT
    file: Optional[Any] = None  # JSONB, can be dict or None


class UpdateMessage(BaseModel):
    content: Optional[str] = None
    file: Optional[Any] = None


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: Optional[int]
    content: str
    file: Optional[Any]
    type: MessageType
    created_at: datetime
    sender: Optional["UserResponse"]

    class Config:
        from_attributes = True
