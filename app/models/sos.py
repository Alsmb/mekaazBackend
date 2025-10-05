# file: app/models/sos.py
from sqlalchemy import Column, DateTime, String, ForeignKey, Text, Boolean, Integer
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class SOS(Base):
    __tablename__ = "sos"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    status = Column(String, default="active")
    emergency_type = Column(String)
    location_lat = Column(String)
    location_lng = Column(String)
    location_address = Column(Text)
    vital_data = Column(Text)
    notes = Column(Text)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolved_by = Column(GUID(), ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "status": self.status,
            "emergency_type": self.emergency_type,
            "location_lat": self.location_lat,
            "location_lng": self.location_lng,
            "location_address": self.location_address,
            "vital_data": self.vital_data,
            "notes": self.notes,
            "triggered_at": self.triggered_at,
            "resolved_at": self.resolved_at,
            "resolved_by": str(self.resolved_by) if self.resolved_by else None
        }

class SOSNotification(Base):
    __tablename__ = "sos_notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sos_id = Column(GUID(), ForeignKey("sos.id"))
    contact_id = Column(GUID(), ForeignKey("emergency_contacts.id"))
    notification_type = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime)
    response_received = Column(Boolean, default=False)
    response_at = Column(DateTime)

    def to_dict(self):
        
        return {
            "id": self.id,
            "sos_id": str(self.sos_id),
            "contact_id": str(self.contact_id),
            "notification_type": self.notification_type,
            "sent_at": self.sent_at,
            "delivered": self.delivered,
            "delivered_at": self.delivered_at,
            "response_received": self.response_received,
            "response_at": self.response_at
        }