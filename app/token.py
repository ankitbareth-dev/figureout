
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from dotenv import load_dotenv

load_dotenv()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user_id: str) -> str:
    secret = os.getenv("JWT_SECRET")

    if secret is None:
        raise RuntimeError("JWT_SECRET is not configured")

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expires_at,
    }

    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    secret = os.getenv("JWT_SECRET")

    if secret is None:
        raise RuntimeError("JWT_SECRET is not configured")

    return jwt.decode(token, secret, algorithms=[ALGORITHM])
