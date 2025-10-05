from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    relationship = Column(String)  # "spouse", "parent", "child", etc.
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert EmergencyContact model to dictionary with string UUIDs"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "phone": self.phone,
            "relationship": self.relationship,
            "is_primary": self.is_primary,
            "created_at": self.created_at
        } 