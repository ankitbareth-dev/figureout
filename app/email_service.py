import os

import resend
from dotenv import load_dotenv

load_dotenv()


def send_otp_email(email: str, otp: str) -> None:
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL")

    if not api_key or not from_email:
        raise RuntimeError("Resend email configuration is missing")

    resend.api_key = api_key

    resend.Emails.send(
        {
            "from": from_email,
            "to": [email],
            "subject": "Verify your Figureout account",
            "html": (
                "<div>"
                "<h2>Verify your email</h2>"
                "<p>Your Figureout verification code is:</p>"
                f"<h1>{otp}</h1>"
                "<p>This code expires in 10 minutes.</p>"
                "</div>"
            ),
        }
    )