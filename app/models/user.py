from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import enum
import uuid
from datetime import datetime
import os

class LanguageEnum(enum.Enum):
    EN = "EN"
    AR = "AR"

class UserRole(str, enum.Enum):
    PATIENT = "patient"
    FAMILY_MEMBER = "family_member"

class User(Base):
    __tablename__ = "users"
    # Use String for development with SQLite
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    language = Column(Enum(LanguageEnum))
    is_phone_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert User model to dictionary with string UUID"""
        return {
            "id": str(self.id),
            "email": self.email,
            "phone_number": self.phone_number,
            "name": self.name,
            "role": self.role,
            "language": self.language,
            "is_phone_verified": self.is_phone_verified,
            "is_email_verified": self.is_email_verified,
            "created_at": self.created_at
        } 