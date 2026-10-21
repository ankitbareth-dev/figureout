
from app.token import create_access_token


def issue_user_token(user_id: str) -> str:
    return create_access_token(user_id)
