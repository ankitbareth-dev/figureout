
from uuid import UUID

from app.database import get_connection


from datetime import datetime


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


def save_pending_registration(
    name: str,
    email: str,
    password_hash: str,
    otp_hash: str,
    expires_at: datetime,
) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO email_verification_otps (
                    name,
                    email,
                    password_hash,
                    otp_hash,
                    expires_at
                )
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (email)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    password_hash = EXCLUDED.password_hash,
                    otp_hash = EXCLUDED.otp_hash,
                    expires_at = EXCLUDED.expires_at,
                    created_at = NOW();
                """,
                (name, email, password_hash, otp_hash, expires_at),
            )


def get_pending_registration(email: str) -> dict | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, email, password_hash, otp_hash, expires_at
                FROM email_verification_otps
                WHERE email = %s;
                """,
                (email,),
            )
            return cursor.fetchone()



def delete_pending_registration(email: str) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM email_verification_otps
                WHERE email = %s;
                """,
                (email,),
            )

def get_user_by_id(user_id: str) -> dict | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, email, password_hash, created_at
                FROM users
                WHERE id = %s;
                """,
                (user_id,),
            )
            return cursor.fetchone()



def delete_expired_pending_registrations() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM email_verification_otps
                WHERE expires_at <= NOW();
                """
            )
