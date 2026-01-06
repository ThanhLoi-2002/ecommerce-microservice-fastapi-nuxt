from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Annotated
from app.core.security import decode_jwt
from app.common.dto.models import TokenPayload
from app.db.models.user import RoleEnum, User
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.db.session import get_db

api_key_header = APIKeyHeader(name="Authorization")

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(api_key_header)]


async def get_current_user(db: AsyncSessionDep, token: TokenDep) -> User:
    if token == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is required"
        )
    try:
        payload = decode_jwt(token)

        token_data = TokenPayload(**payload)
    except Exception as e:
        logger.exception(
            "Unexpected error in get_current_user | Error: {e}",
            e=e,
        )
        raise HTTPException(status_code=401, detail="Token is expired")

    user = await db.get(User, token_data.id)

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

def roles_required(roles: list[RoleEnum]):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user
    return role_checker
