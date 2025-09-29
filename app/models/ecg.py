from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime

class ECG(Base):
    __tablename__ = "ecgs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"))
    recording_duration = Column(String, default="30_seconds")  # "30_seconds", "60_seconds"
    ecg_data = Column(Text)  # JSON string of ECG readings
    pdf_url = Column(String)  # S3/Supabase URL for generated PDF
    status = Column(String, default="recording")  # "recording", "processing", "completed", "failed"
    recording_started_at = Column(DateTime, default=datetime.utcnow)
    recording_completed_at = Column(DateTime)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    file_size = Column(Integer)  # PDF file size in bytes
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert ECG model to dictionary with string UUIDs"""
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ecg_id = Column(UUID(as_uuid=True), ForeignKey("ecgs.id"))
    session_type = Column(String)  # "single_lead", "multi_lead"
    lead_count = Column(Integer, default=1)
    sampling_rate = Column(Integer, default=500)  # Hz
    resolution = Column(Integer, default=12)  # bits
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert ECGSession model to dictionary with string UUIDs"""
        return {
            "id": str(self.id),
            "ecg_id": str(self.ecg_id),
            "session_type": self.session_type,
            "lead_count": self.lead_count,
            "sampling_rate": self.sampling_rate,
            "resolution": self.resolution,
            "created_at": self.created_at
        } 