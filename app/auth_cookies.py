
import os

from fastapi import Response


ACCESS_TOKEN_COOKIE = "figureout_access_token"
ACCESS_TOKEN_MAX_AGE = 30 * 60


def set_auth_cookie(response: Response, token: str) -> None:
    is_production = os.getenv("ENVIRONMENT") == "production"

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=token,
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=True,
        secure=is_production,
        samesite="lax",
        path="/",
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=ACCESS_TOKEN_COOKIE,
        httponly=True,
        secure=os.getenv("ENVIRONMENT") == "production",
        samesite="lax",
        path="/",
    )
