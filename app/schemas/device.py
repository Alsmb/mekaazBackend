from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DeviceResponse(BaseModel):
    id: str
    user_id: str
    device_type: str
    device_id: str
    device_name: Optional[str]
    is_connected: bool
    last_connected: Optional[datetime]
    created_at: datetime

class DeviceConnectRequest(BaseModel):
    device_id: str
    device_type: str
    device_name: Optional[str] = None

class DeviceStatusResponse(BaseModel):
    id: str
    user_id: str
    device_type: str
    device_id: str
    device_name: Optional[str]
    is_connected: bool
    last_connected: Optional[datetime]
    created_at: datetime

class AvailableDeviceResponse(BaseModel):
    device_id: str
    device_type: str
    device_name: Optional[str]
    is_available: bool

class DeviceListResponse(BaseModel):
    devices: List[DeviceResponse] 