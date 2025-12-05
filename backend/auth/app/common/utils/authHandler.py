import jwt
import time
from .timeHelper import parse_duration
from app.core.config import settings

class AuthHandler(object):
    @staticmethod
    def sign_jwt(data: dict) -> str:
        payload = {
            **data,  # merge data
            "expires": int(time.time()) + parse_duration(settings.ACCESS_TOKEN_EXPIRE),
        }

        token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except Exception as e:
            print("Error:", e)
            # display all error lines
            # print(traceback.format_exc())
