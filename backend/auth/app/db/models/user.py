from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum
from sqlalchemy.orm import relationship

from app.db.base import Base


class RoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String(70), unique=True)
    password = Column(String(255))
    name = Column(String(255))
    avatar = Column(JSONB, nullable=True)
    role = Column(SqlEnum(RoleEnum), nullable=False, default=RoleEnum.USER)