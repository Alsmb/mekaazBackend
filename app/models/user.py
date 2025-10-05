# file: app/models/user.py
from sqlalchemy import Column, String, DateTime, Enum, Boolean
from app.core.custom_types import GUID
from app.core.database import Base
import enum
import uuid
from datetime import datetime

class LanguageEnum(enum.Enum):
    EN = "EN"
    AR = "AR"

class UserRole(str, enum.Enum):
    PATIENT = "patient"
    FAMILY_MEMBER = "family_member"

class User(Base):
    __tablename__ = "users"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
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
        
        return {
            "id": str(self.id),
            "email": self.email,
            "phone_number": self.phone_number,
            "name": self.name,
            "role": self.role.value if self.role else None,
            "language": self.language.value if self.language else None,
            "is_phone_verified": self.is_phone_verified,
            "is_email_verified": self.is_email_verified,
            "created_at": self.created_at
        }