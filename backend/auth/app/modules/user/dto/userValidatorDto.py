from pydantic import BaseModel, EmailStr, Field

class CreateUserDto(BaseModel):
    name: str = Field(..., min_length=2)# ... = required
    email: EmailStr
    password: str = Field(..., min_length=6)
