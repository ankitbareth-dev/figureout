
from uuid import UUID

from app.database import get_connection


def get_user_by_email(email: str) -> dict | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, email, password_hash, created_at
                FROM users
                WHERE email = %s;
                """,
                (email,),
            )
            user = cursor.fetchone()

    if user is None:
        return None

    return {
        **user,
        "id": UUID(str(user["id"])),
    }
