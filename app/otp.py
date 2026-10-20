
import hashlib
import hmac
import os
import secrets

from dotenv import load_dotenv

load_dotenv()


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(otp: str) -> str:
    secret = os.getenv("OTP_HASH_SECRET")

    if secret is None:
        raise RuntimeError("OTP_HASH_SECRET is not configured")

    return hmac.new(
        secret.encode(),
        otp.encode(),
        hashlib.sha256,
    ).hexdigest()


def verify_otp(otp: str, hashed_otp: str) -> bool:
    return hmac.compare_digest(hash_otp(otp), hashed_otp)
