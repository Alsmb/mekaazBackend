from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    otp_code = Column(String, nullable=False)
    otp_type = Column(String, nullable=False)  # "phone" or "email"
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert OTP model to dictionary with integer ID"""
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "otp_code": self.otp_code,
            "otp_type": self.otp_type,
            "expires_at": self.expires_at,
            "is_used": self.is_used,
            "created_at": self.created_at
        } 