from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from sqlalchemy.orm import relationship

class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    BOTH = "BOTH"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    img = Column(JSONB, nullable=True)
    pid = Column(Integer, ForeignKey("categories.id"), nullable=True)
    gender = Column(SqlEnum(GenderEnum))
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Self-referential relationship
    parent = relationship("Category", remote_side=[id], backref="children")

    # def __repr__(self):
    #     return f"<Category(id={self.id}, name={self.name}, slug={self.slug})>"
