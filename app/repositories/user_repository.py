
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


def create_user(
    name: str,
    email: str,
    password_hash: str | None,
) -> dict:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, created_at;
                """,
                (name, email, password_hash),
            )
            user = cursor.fetchone()

    if user is None:
        raise RuntimeError("User creation failed")

    return user
