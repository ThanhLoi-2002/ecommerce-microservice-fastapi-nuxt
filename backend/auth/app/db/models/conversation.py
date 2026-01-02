from sqlalchemy import Column, DateTime, Integer, String, Table, ForeignKey, Text, func
from app.db.base import Base
import enum
from sqlalchemy.orm import relationship


class ConversationType(enum.Enum):
    PRIVATE = "private"
    GROUP = "group"


conversation_members = Table(
    "conversation_members",
    Base.metadata,
    Column(
        "conversation_id", Integer, ForeignKey("conversations.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

conversation_admins = Table(
    "conversation_admins",
    Base.metadata,
    Column(
        "conversation_id", Integer, ForeignKey("conversations.id"), primary_key=True
    ),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    # Tên nhóm (private có thể null)
    name = Column(String(255), nullable=True, index=True)

    # Avatar nhóm / avatar cuộc trò chuyện
    avatar = Column(String(255), nullable=True)

    # Loại conversation
    type = Column(enum.Enum(ConversationType), nullable=False)

    # Nhóm trưởng
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Tin nhắn cuối
    last_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # ================= Relationships =================

    # Thành viên
    members = relationship(
        "User", secondary="conversation_members", back_populates="conversations"
    )

    # Nhóm trưởng
    owner = relationship("User", foreign_keys=[owner_id])

    # Nhóm phó (many-to-many)
    admins = relationship(
        "User", secondary="conversation_admins", back_populates="admin_conversations"
    )

    # Tin nhắn cuối
    last_message = relationship("Message", foreign_keys=[last_message_id])


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
