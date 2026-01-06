from sqlalchemy import Column, DateTime, Integer, String, Table, ForeignKey, Text, func, Enum as SqlEnum
from app.db.base import Base
from enum import Enum
from sqlalchemy.orm import relationship


class ConversationType(str, Enum):
    PRIVATE = "PRIVATE"
    GROUP = "GROUP"

class AdminRole(str, Enum):
    LEADER = "LEADER"
    DEPUTY = "DEPUTY"

conversation_members = Table(
    "conversation_members",
    Base.metadata,
    Column(
        "conversation_id", Integer, ForeignKey("conversations.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("last_read_message_id", Integer, ForeignKey("messages.id"), primary_key=True)
)

class ConversationAdmins(Base):
    __tablename__ = "conversation_admins"

    conversation_id = Column(Integer, ForeignKey("conversations.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(SqlEnum(AdminRole), nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="admins")
    user = relationship("User", back_populates="admin_conversations")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    # Tên nhóm (private có thể null)
    name = Column(String(255), nullable=True, index=True)

    # Avatar nhóm / avatar cuộc trò chuyện
    avatar = Column(String(255), nullable=True)

    # Loại conversation
    type = Column(SqlEnum(ConversationType), nullable=False)

    # Nhóm trưởng
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Tin nhắn cuối
    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ================= Relationships =================

    members = relationship("User", secondary=conversation_members, back_populates="conversations")
    owner = relationship("User", foreign_keys=[owner_id])
    admins = relationship("ConversationAdmins", back_populates="conversation")
    last_message = relationship("Message", foreign_keys=[last_message_id])
