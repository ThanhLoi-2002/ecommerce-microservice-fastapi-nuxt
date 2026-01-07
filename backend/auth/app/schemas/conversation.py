from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from app.db.models.conversation import ConversationType
from app.schemas.type import Image
from app.schemas.user import UserResponse  # Import here to avoid circular import


class CreateConversation(BaseModel):
    type: ConversationType = Field(...)
    name: Optional[str] = None  # Required for GROUP, optional for PRIVATE
    avatar: Optional[Image] = None  # Avatar data with public_id and url
    member_ids: List[int] = Field(
        ..., min_items=1
    )  # List of user IDs to add as members


class UpdateConversation(BaseModel):
    name: Optional[str] = None
    avatar: Optional[Image] = None  # Avatar data with public_id and url


class ConversationAdmin(BaseModel):
    user_id: int
    role: str

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: int
    name: Optional[str]
    avatar: Optional[Image]  # Avatar data with public_id and url
    type: ConversationType
    owner_id: Optional[int]
    last_message_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    members: List["UserResponse"]  # Forward reference
    admins: List[ConversationAdmin]

    class Config:
        from_attributes = True

