
import jwt
from fastapi import Cookie, HTTPException, status

from app.auth_cookies import ACCESS_TOKEN_COOKIE
from app.repositories.user_repository import get_user_by_id
from app.token import decode_access_token


def get_current_user(
    token: str | None = Cookie(default=None, alias=ACCESS_TOKEN_COOKIE),
) -> dict:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        ) from None

    user_id = payload.get("sub")

    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return {
        "id": str(user["id"]),
        "name": user["name"],
        "email": user["email"],
    }
