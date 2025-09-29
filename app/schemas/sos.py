from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SOSResponse(BaseModel):
    id: str
    user_id: str
    status: str
    emergency_type: Optional[str]
    location_lat: Optional[str]
    location_lng: Optional[str]
    location_address: Optional[str]
    vital_data: Optional[str]
    notes: Optional[str]
    triggered_at: datetime
    resolved_at: Optional[datetime]
    resolved_by: Optional[str]

class SOSTriggerRequest(BaseModel):
    emergency_type: str = "medical"
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    location_address: Optional[str] = None
    notes: Optional[str] = None

class SOSCancelRequest(BaseModel):
    reason: Optional[str] = None

class SOSResolveRequest(BaseModel):
    resolved_by: str
    resolution_notes: Optional[str] = None

class SOSNotificationResponse(BaseModel):
    id: str
    sos_id: str
    contact_id: str
    notification_type: str
    sent_at: datetime
    delivered: bool
    delivered_at: Optional[datetime]
    response_received: bool
    response_at: Optional[datetime]

class SOSHistoryResponse(BaseModel):
    sos_alerts: List[SOSResponse]
    total_count: int 