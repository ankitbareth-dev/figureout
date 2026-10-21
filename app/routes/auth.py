
from fastapi import APIRouter, HTTPException, Response, status, Depends

from app.auth_cookies import clear_auth_cookie, set_auth_cookie
from app.schemas.auth import LoginRequest, RegisterRequest, VerifyOTPRequest
from app.services.auth_service import (
    login_user,
    register_user,
    verify_registration_otp,
    
)
from app.auth_dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_202_ACCEPTED)
def register(data: RegisterRequest):
    try:
        register_user(data.name, str(data.email), data.password)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return {"message": "Registration pending OTP verification"}


@router.post("/verify-otp")
def verify_otp(data: VerifyOTPRequest, response: Response):
    try:
        result = verify_registration_otp(str(data.email), data.otp)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    set_auth_cookie(response, result["access_token"])

    return {
        "id": result["id"],
        "name": result["name"],
        "email": result["email"],
    }


@router.post("/login")
def login(data: LoginRequest, response: Response):
    try:
        result = login_user(str(data.email), data.password)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error

    set_auth_cookie(response, result["access_token"])

    return {
        "id": result["id"],
        "name": result["name"],
        "email": result["email"],
    }


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookie(response)
    return {"message": "Logged out successfully"}


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

