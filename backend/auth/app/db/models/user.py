from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.friendship import Friendship


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(70), unique=True)
    password = Column(String(255))
    name = Column(String(255))
    avatar = Column(JSONB, nullable=True)
    role = Column(SqlEnum(RoleEnum), nullable=False, default=RoleEnum.USER)

    conversations = relationship(
        "Conversation", secondary="conversation_members", back_populates="members"
    )
    admin_conversations = relationship("ConversationAdmins", back_populates="user")
    friends = relationship(
        "Friendship",
        primaryjoin="or_(User.id==Friendship.user_id_1, User.id==Friendship.user_id_2)",
        back_populates="users"
    )
    friends = relationship("Friendship", foreign_keys=[Friendship.user_id], back_populates="user")
    friend_of = relationship("Friendship", foreign_keys=[Friendship.friend_id], back_populates="friend")

