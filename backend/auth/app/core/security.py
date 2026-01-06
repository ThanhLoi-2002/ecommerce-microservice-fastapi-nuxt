import jwt
import time
from ..utils.timeHelper import parse_duration
from app.core.config import settings


def createToken(data: dict) -> str:
    payload = {
        **data,  # merge data
        "exp": int(time.time()) + parse_duration(settings.ACCESS_TOKEN_EXPIRE),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def createRefreshToken(data: dict) -> str:
    payload = {
        **data,  # merge data
        "exp": int(time.time()) + parse_duration(settings.REFRESH_TOKEN_EXPIRE),
    }

    token = jwt.encode(payload, settings.REFRESH_TOKEN, algorithm=settings.ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        return None
    
def decode_refresh_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.REFRESH_TOKEN, algorithms=[settings.ALGORITHM]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        return None


def refreshToken(refreshToken: str) -> str:
    try:
        decoded_token = jwt.decode(
            refreshToken, settings.REFRESH_TOKEN, algorithms=[settings.ALGORITHM]
        )
        if decoded_token["exp"] >= time.time():
            return createToken(decoded_token)
        else:
            return None

    except Exception as e:
        print("Error:", e)
        return None
