# file: app/models/device.py
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class Device(Base):
    __tablename__ = "devices"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    device_type = Column(String, nullable=False)
    device_id = Column(String, unique=True, nullable=False)
    device_name = Column(String)
    is_connected = Column(Boolean, default=False)
    last_connected = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "device_type": self.device_type,
            "device_id": self.device_id,
            "device_name": self.device_name,
            "is_connected": self.is_connected,
            "last_connected": self.last_connected,
            "created_at": self.created_at
        }