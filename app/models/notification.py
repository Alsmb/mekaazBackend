# file: app/models/notification.py
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(GUID(), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, default="general")
    severity = Column(String, default="info")
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "severity": self.severity,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }