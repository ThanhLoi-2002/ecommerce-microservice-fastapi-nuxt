import jwt
from datetime import datetime, timedelta
from ..config.config import settings

def create_token(data: dict, expires_minutes=30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)