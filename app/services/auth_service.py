
from datetime import datetime, timezone

from app.otp import verify_otp
from app.repositories.user_repository import (
    create_user,
    delete_pending_registration,
    get_pending_registration,
)


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
