from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text, func, Enum as SqlEnum
from app.db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB

class MessageType(str, Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    FILE = "FILE"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    file = Column(JSONB)
    type = Column(SqlEnum(MessageType), default=MessageType.TEXT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id])