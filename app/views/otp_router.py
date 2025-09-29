from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.otp import SendOTPRequest, VerifyOTPRequest, OTPResponse, OTPVerificationResponse
from app.controllers.otp_controller import OTPController

router = APIRouter(prefix="/auth", tags=["OTP"])

@router.post("/send-otp", response_model=OTPResponse)
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to email or phone"""
    return OTPController.send_otp(
        db=db,
        email=data.email,
        phone_number=data.phone_number,
        otp_type=data.otp_type
    )

@router.post("/verify-otp", response_model=OTPVerificationResponse)
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP for email or phone"""
    return OTPController.verify_otp(
        db=db,
        email=data.email,
        phone_number=data.phone_number,
        otp_code=data.otp_code,
        otp_type=data.otp_type
    ) 