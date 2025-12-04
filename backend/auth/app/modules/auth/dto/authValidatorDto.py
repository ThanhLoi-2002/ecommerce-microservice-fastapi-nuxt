from pydantic import BaseModel, EmailStr, Field

class LoginDto(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class SignUpDto(BaseModel):
    name: str = Field(..., min_length=2)# ... = required
    email: EmailStr
    password: str = Field(..., min_length=6)