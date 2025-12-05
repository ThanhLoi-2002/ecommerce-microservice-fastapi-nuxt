from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from typing import Annotated
from app.common.utils.authHandler import AuthHandler
from app.core.db import get_db
from app.common.dto.models import TokenPayload
from app.modules.user.userModel import User
from sqlalchemy.orm import Session

api_key_header = APIKeyHeader(name="X-API-KEY")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(api_key_header)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    print("token: ", token)
    try:
        payload = AuthHandler.decode_jwt(token)

        if payload == None:
            raise HTTPException(status_code=401, detail="Token is expired")
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
