from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    img = Column(String, nullable=True)
    pid = Column(Integer, ForeignKey("categories.id"), nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Self-referential relationship
    parent = relationship("Category", remote_side=[id], backref="children")

    # def __repr__(self):
    #     return f"<Category(id={self.id}, name={self.name}, slug={self.slug})>"
