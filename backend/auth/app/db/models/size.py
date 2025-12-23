from sqlalchemy import (
    Column,
    Integer,
    String,
)
from app.db.base import Base

class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
