from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class VitalResponse(BaseModel):
    id: str
    user_id: str
    device_id: Optional[str]
    heart_rate: Optional[int]
    spo2: Optional[float]
    temperature: Optional[float]
    steps: Optional[int]
    blood_pressure_systolic: Optional[int]
    blood_pressure_diastolic: Optional[int]
    respiratory_rate: Optional[int]
    health_condition: Optional[str]
    is_anomaly: bool
    timestamp: datetime

class VitalIngestRequest(BaseModel):
    device_id: str
    heart_rate: Optional[int] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    steps: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    respiratory_rate: Optional[int] = None

class VitalHistoryRequest(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = 100

class VitalAggregateResponse(BaseModel):
    id: str
    user_id: str
    aggregate_type: str
    heart_rate_avg: Optional[float]
    heart_rate_min: Optional[int]
    heart_rate_max: Optional[int]
    spo2_avg: Optional[float]
    spo2_min: Optional[float]
    spo2_max: Optional[float]
    temperature_avg: Optional[float]
    temperature_min: Optional[float]
    temperature_max: Optional[float]
    steps_total: Optional[int]
    anomaly_count: int
    start_time: datetime
    end_time: datetime

class ChartDataResponse(BaseModel):
    period: str  # "hour", "day", "week"
    data: List[Dict[str, Any]]  # Flexible data structure

class LiveVitalResponse(BaseModel):
    heart_rate: Optional[int]
    spo2: Optional[float]
    temperature: Optional[float]
    steps: Optional[int]
    health_condition: str
    is_anomaly: bool
    timestamp: datetime 