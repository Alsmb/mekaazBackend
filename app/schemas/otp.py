from pydantic import BaseModel, EmailStr
from typing import Optional

class SendOTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    otp_type: str  # "phone" or "email"

class VerifyOTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    otp_code: str
    otp_type: str  # "phone" or "email"

class OTPResponse(BaseModel):
    message: str
    expires_in: int  # seconds

class OTPVerificationResponse(BaseModel):
    message: str
    is_verified: bool 