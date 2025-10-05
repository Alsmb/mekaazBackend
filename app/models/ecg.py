# file: app/models/ecg.py
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Integer
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class ECG(Base):
    __tablename__ = "ecgs"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    device_id = Column(GUID(), ForeignKey("devices.id"))
    recording_duration = Column(String, default="30_seconds")
    ecg_data = Column(Text)
    pdf_url = Column(String)
    status = Column(String, default="recording")
    recording_started_at = Column(DateTime, default=datetime.utcnow)
    recording_completed_at = Column(DateTime)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):

        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "device_id": str(self.device_id) if self.device_id else None,
            "recording_duration": self.recording_duration,
            "ecg_data": self.ecg_data,
            "pdf_url": self.pdf_url,
            "status": self.status,
            "recording_started_at": self.recording_started_at,
            "recording_completed_at": self.recording_completed_at,
            "processing_started_at": self.processing_started_at,
            "processing_completed_at": self.processing_completed_at,
            "file_size": self.file_size,
            "created_at": self.created_at
        }

class ECGSession(Base):
    __tablename__ = "ecg_sessions"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    ecg_id = Column(GUID(), ForeignKey("ecgs.id"))
    session_type = Column(String)
    lead_count = Column(Integer, default=1)
    sampling_rate = Column(Integer, default=500)
    resolution = Column(Integer, default=12)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        
        return {
            "id": str(self.id),
            "ecg_id": str(self.ecg_id),
            "session_type": self.session_type,
            "lead_count": self.lead_count,
            "sampling_rate": self.sampling_rate,
            "resolution": self.resolution,
            "created_at": self.created_at
        }