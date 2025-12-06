# JSON payload containing access token
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    id: int | None = None
    exp: int
