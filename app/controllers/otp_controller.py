from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.otp import OTP
from app.models.user import User
from app.services.sms_service import SMSService
from app.services.email_service import EmailService
import uuid

class OTPController:
    @staticmethod
    def send_otp(db: Session, email: str = None, phone_number: str = None, otp_type: str = "email"):
        """Send OTP to email or phone"""
        
        # Validate input
        if otp_type == "email" and not email:
            raise HTTPException(status_code=400, detail="Email is required for email OTP")
        if otp_type == "phone" and not phone_number:
            raise HTTPException(status_code=400, detail="Phone number is required for phone OTP")
        
        # Find user
        user = None
        if email:
            user = db.query(User).filter_by(email=email).first()
        elif phone_number:
            user = db.query(User).filter_by(phone_number=phone_number).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate OTP
        if otp_type == "email":
            otp_code = EmailService.generate_otp()
        else:
            otp_code = SMSService.generate_otp()
        
        # Create OTP record
        otp = OTP(
            id=str(uuid.uuid4()),
            user_id=user.id,
            otp_code=otp_code,
            otp_type=otp_type,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            created_at=datetime.utcnow()
        )
        
        db.add(otp)
        db.commit()
        
        # Send OTP
        if otp_type == "email":
            EmailService.send_otp(email, otp_code)
        else:
            SMSService.send_otp(phone_number, otp_code)
        
        return {"message": f"OTP sent to {email or phone_number}", "expires_in": 600}
    
    @staticmethod
    def verify_otp(db: Session, email: str = None, phone_number: str = None, otp_code: str = None, otp_type: str = "email"):
        """Verify OTP"""
        
        # Find user
        user = None
        if email:
            user = db.query(User).filter_by(email=email).first()
        elif phone_number:
            user = db.query(User).filter_by(phone_number=phone_number).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find valid OTP
        otp = db.query(OTP).filter(
            OTP.user_id == user.id,
            OTP.otp_code == otp_code,
            OTP.otp_type == otp_type,
            OTP.is_used == False,
            OTP.expires_at > datetime.utcnow()
        ).first()
        
        if not otp:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        
        # Mark OTP as used
        otp.is_used = True
        db.commit()
        
        # Update user verification status
        if otp_type == "email":
            user.is_email_verified = True
        else:
            user.is_phone_verified = True
        
        db.commit()
        
        return {"message": f"{otp_type.capitalize()} verified successfully", "is_verified": True} 