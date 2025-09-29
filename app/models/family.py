from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class Family(Base):
    __tablename__ = "families"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    invite_code = Column(String, unique=True)
    family_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert Family model to dictionary with string UUIDs"""
        return {
            "id": str(self.id),
            "owner_id": str(self.owner_id),
            "invite_code": self.invite_code,
            "family_name": self.family_name,
            "created_at": self.created_at
        }

class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    member_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role = Column(String, default="member")  # "owner", "member"
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def to_dict(self):
        """Convert FamilyMember model to dictionary with string UUIDs"""
        return {
            "id": str(self.id),
            "owner_id": str(self.owner_id),
            "member_id": str(self.member_id),
            "role": self.role,
            "joined_at": self.joined_at,
            "is_active": self.is_active
        }

class FamilySharingSettings(Base):
    __tablename__ = "family_sharing_settings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"))
    share_heart_rate = Column(Boolean, default=True)
    share_spo2 = Column(Boolean, default=True)
    share_temperature = Column(Boolean, default=True)
    share_steps = Column(Boolean, default=True)
    share_blood_pressure = Column(Boolean, default=True)
    share_respiratory_rate = Column(Boolean, default=True)
    share_ecg = Column(Boolean, default=False)
    share_sos_alerts = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert FamilySharingSettings model to dictionary with string UUIDs"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "family_id": str(self.family_id),
            "share_heart_rate": self.share_heart_rate,
            "share_spo2": self.share_spo2,
            "share_temperature": self.share_temperature,
            "share_steps": self.share_steps,
            "share_blood_pressure": self.share_blood_pressure,
            "share_respiratory_rate": self.share_respiratory_rate,
            "share_ecg": self.share_ecg,
            "share_sos_alerts": self.share_sos_alerts,
            "updated_at": self.updated_at
        } 