# file: app/models/vitals.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Text, Boolean
from app.core.custom_types import GUID
from app.core.database import Base
import uuid
from datetime import datetime

class Vital(Base):
    __tablename__ = "vitals"
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id"))
    device_id = Column(GUID(), ForeignKey("devices.id"))
    heart_rate = Column(Integer)
    spo2 = Column(Float)
    temperature = Column(Float)
    steps = Column(Integer)
    blood_pressure_systolic = Column(Integer)
    blood_pressure_diastolic = Column(Integer)
    respiratory_rate = Column(Integer)
    health_condition = Column(String)
    is_anomaly = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "device_id": str(self.device_id) if self.device_id else None,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "temperature": self.temperature,
            "steps": self.steps,
            "blood_pressure_systolic": self.blood_pressure_systolic,
            "blood_pressure_diastolic": self.blood_pressure_diastolic,
            "respiratory_rate": self.respiratory_rate,
            "health_condition": self.health_condition,
            "is_anomaly": self.is_anomaly,
            "timestamp": self.timestamp
        }

class VitalAggregate(Base):
    __tablename__ = "vital_aggregates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(GUID(), ForeignKey("users.id"))
    aggregate_type = Column(String)
    heart_rate_avg = Column(Float)
    heart_rate_min = Column(Integer)
    heart_rate_max = Column(Integer)
    spo2_avg = Column(Float)
    spo2_min = Column(Float)
    spo2_max = Column(Float)
    temperature_avg = Column(Float)
    temperature_min = Column(Float)
    temperature_max = Column(Float)
    steps_total = Column(Integer)
    anomaly_count = Column(Integer, default=0)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": str(self.user_id),
            "aggregate_type": self.aggregate_type,
            "heart_rate_avg": self.heart_rate_avg,
            "heart_rate_min": self.heart_rate_min,
            "heart_rate_max": self.heart_rate_max,
            "spo2_avg": self.spo2_avg,
            "spo2_min": self.spo2_min,
            "spo2_max": self.spo2_max,
            "temperature_avg": self.temperature_avg,
            "temperature_min": self.temperature_min,
            "temperature_max": self.temperature_max,
            "steps_total": self.steps_total,
            "anomaly_count": self.anomaly_count,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "created_at": self.created_at
        }