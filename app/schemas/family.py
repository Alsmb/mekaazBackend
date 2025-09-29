from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FamilyResponse(BaseModel):
    id: str
    owner_id: str
    invite_code: Optional[str]
    family_name: Optional[str]
    created_at: datetime

class FamilyMemberResponse(BaseModel):
    id: str
    owner_id: str
    member_id: str
    role: str
    joined_at: datetime
    is_active: bool
    member_name: Optional[str]
    member_email: Optional[str]

class FamilyInviteRequest(BaseModel):
    family_name: Optional[str] = None

class FamilyJoinRequest(BaseModel):
    invite_code: str

class FamilySharingSettingsResponse(BaseModel):
    id: str
    user_id: str
    family_id: str
    share_heart_rate: bool
    share_spo2: bool
    share_temperature: bool
    share_steps: bool
    share_blood_pressure: bool
    share_respiratory_rate: bool
    share_ecg: bool
    share_sos_alerts: bool
    updated_at: datetime

class FamilySharingSettingsUpdateRequest(BaseModel):
    share_heart_rate: Optional[bool] = None
    share_spo2: Optional[bool] = None
    share_temperature: Optional[bool] = None
    share_steps: Optional[bool] = None
    share_blood_pressure: Optional[bool] = None
    share_respiratory_rate: Optional[bool] = None
    share_ecg: Optional[bool] = None
    share_sos_alerts: Optional[bool] = None

class FamilyMemberHealthResponse(BaseModel):
    member_id: str
    member_name: str
    latest_vitals: dict
    health_condition: str
    last_updated: datetime 