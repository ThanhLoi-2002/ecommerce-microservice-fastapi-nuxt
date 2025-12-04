from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    role: str
    avatar: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2
