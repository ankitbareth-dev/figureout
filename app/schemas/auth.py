from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(pattern=r"^[0-9]{6}$")
