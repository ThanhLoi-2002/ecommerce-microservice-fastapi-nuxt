import jwt
from ..config.config import settings
import time
from .timeHelper import parse_duration


class AuthHandler(object):
    @staticmethod
    def sign_jwt(data: dict) -> str:
        payload = {
            **data,  # merge data
            "expires": int(time.time()) + parse_duration(settings.JWT_EXPRIES),
        }

        token = jwt.encode(
            payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except Exception as e:
            print("Error:", e)
            # display all error lines
            # print(traceback.format_exc())
