from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ECGResponse(BaseModel):
    id: str
    user_id: str
    device_id: Optional[str]
    recording_duration: str
    status: str
    recording_started_at: Optional[datetime]
    recording_completed_at: Optional[datetime]
    processing_started_at: Optional[datetime]
    processing_completed_at: Optional[datetime]
    pdf_url: Optional[str]
    file_size: Optional[int]
    created_at: datetime

class ECGStartRequest(BaseModel):
    device_id: str
    recording_duration: str = "30_seconds"
    session_type: str = "single_lead"
    lead_count: int = 1
    sampling_rate: int = 500
    resolution: int = 12

class ECGDataRequest(BaseModel):
    ecg_id: str
    ecg_data: Dict[str, Any]  # JSON data from device

class ECGCompleteRequest(BaseModel):
    ecg_id: str
    final_data: Dict[str, Any]  # Final ECG data

class ECGSessionResponse(BaseModel):
    id: str
    ecg_id: str
    session_type: str
    lead_count: int
    sampling_rate: int
    resolution: int
    created_at: datetime

class ECGDownloadResponse(BaseModel):
    download_url: str
    expires_at: datetime
    file_size: int

class ECGAnalysisResponse(BaseModel):
    ecg_id: str
    heart_rate: Optional[int]
    rhythm: str  # "normal", "irregular", "bradycardia", "tachycardia"
    abnormalities: List[str]
    confidence_score: float
    analysis_completed_at: datetime 