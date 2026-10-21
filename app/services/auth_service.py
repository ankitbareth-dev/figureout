
from datetime import datetime, timedelta, timezone
from app.security import verify_password


from fastapi import Response

from app.auth_cookies import clear_auth_cookie

from app.otp import generate_otp, hash_otp, verify_otp
from app.repositories.user_repository import (
    create_user,
    delete_pending_registration,
    get_pending_registration,
    get_user_by_email,
    save_pending_registration,
)
from app.security import hash_password


def verify_registration_otp(email: str, otp: str) -> dict:
    pending = get_pending_registration(email)

    if pending is None:
        raise ValueError("No pending registration found")

    if pending["expires_at"] <= datetime.now(timezone.utc):
        delete_pending_registration(email)
        raise ValueError("OTP has expired")

    if not verify_otp(otp, pending["otp_hash"]):
        raise ValueError("Invalid OTP")

    user = create_user(
        name=pending["name"],
        email=pending["email"],
        password_hash=pending["password_hash"],
    )

    delete_pending_registration(email)

    return user


def register_user(name: str, email: str, password: str) -> None:
    existing_user = get_user_by_email(email)

    if existing_user is not None:
        raise ValueError("An account with this email already exists")

    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    hashed_password = hash_password(password)

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    save_pending_registration(
        name=name,
        email=email,
        password_hash=hashed_password,
        otp_hash=hashed_otp,
        expires_at=expires_at,
    )

def login_user(email: str, password: str) -> dict:
    user = get_user_by_email(email)

    if user is None or user["password_hash"] is None:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password")

    return {
        "id": str(user["id"]),
        "name": user["name"],
        "email": user["email"],
    }


def logout_user(response: Response) -> None:
    clear_auth_cookie(response)
