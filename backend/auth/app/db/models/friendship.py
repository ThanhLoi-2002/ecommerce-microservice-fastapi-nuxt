from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Thiết lập mối quan hệ với người dùng
    user = relationship("User", foreign_keys=[user_id], back_populates="friends")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friend_of")

    # Đảm bảo rằng không có quan hệ bạn bè nào bị trùng lặp
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="uq_user_friend"),
    )