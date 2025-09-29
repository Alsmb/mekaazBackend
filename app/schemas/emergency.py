from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EmergencyContactResponse(BaseModel):
    id: str
    user_id: str
    name: str
    phone: str
    relationship: Optional[str]
    is_primary: bool
    created_at: datetime

class EmergencyContactCreateRequest(BaseModel):
    name: str
    phone: str
    relationship: Optional[str] = None
    is_primary: bool = False

class EmergencyContactUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None
    is_primary: Optional[bool] = None

class EmergencyContactListResponse(BaseModel):
    contacts: List[EmergencyContactResponse] 