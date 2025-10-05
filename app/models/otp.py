# file: app/models/otp.py
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(GUID(), ForeignKey("users.id"))
    otp_code = Column(String, nullable=False)
    otp_type = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "otp_code": self.otp_code,
            "otp_type": self.otp_type,
            "expires_at": self.expires_at,
            "is_used": self.is_used,
            "created_at": self.created_at
        }