from sqlalchemy import (
    Column,
    Integer,
    String,
)
from app.db.base import Base

class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
