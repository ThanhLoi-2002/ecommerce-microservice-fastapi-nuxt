import jwt
import time
from ..utils.timeHelper import parse_duration
from app.core.config import settings


def sign_jwt(data: dict) -> str:
    payload = {
        **data,  # merge data
        "exp": int(time.time()) + parse_duration(settings.ACCESS_TOKEN_EXPIRE),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print("Error:", e)
        # display all error lines
        # print(traceback.format_exc())
        return None
