from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.device import DeviceResponse, DeviceConnectRequest, DeviceStatusResponse
from app.controllers.device_controller import DeviceController

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/connect", response_model=DeviceResponse)
def connect_device(
    data: DeviceConnectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect a device to user"""
    return DeviceController.connect_device(db, str(current_user.id), data.device_id, data.device_type, data.device_name)

@router.get("/available", response_model=list[DeviceResponse])
def get_available_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of available devices for user"""
    return DeviceController.get_available_devices(db, str(current_user.id))

@router.delete("/{device_id}")
def disconnect_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect a device"""
    return DeviceController.disconnect_device(db, str(current_user.id), device_id)

@router.get("/{device_id}/status", response_model=DeviceStatusResponse)
def get_device_status(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device connection status"""
    return DeviceController.get_device_status(db, str(current_user.id), device_id)

# NEW ENDPOINTS FOR FRONTEND COMPATIBILITY

@router.get("/discover")
def discover_bluetooth_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Discover nearby Bluetooth devices (like Mekaaz-1001, Mekaaz-1002, etc.)"""
    return DeviceController.discover_bluetooth_devices()

@router.get("/{device_id}/signal-strength")
def get_device_signal_strength(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get signal strength for a specific device"""
    return DeviceController.get_signal_strength(device_id)

@router.get("/{device_id}/battery")
def get_device_battery(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get battery level for a specific device"""
    return DeviceController.get_battery_level(device_id)

@router.post("/{device_id}/pair")
def pair_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pair with a discovered Bluetooth device"""
    return DeviceController.pair_bluetooth_device(db, str(current_user.id), device_id)

@router.get("/{device_id}/firmware")
def get_device_firmware(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device firmware information"""
    return DeviceController.get_device_firmware(db, str(current_user.id), device_id)

@router.post("/{device_id}/update")
def update_device_firmware(
    device_id: str,
    update_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update device firmware"""
    return DeviceController.update_device_firmware(db, str(current_user.id), device_id, update_data)

@router.get("/{device_id}/calibration")
def get_device_calibration(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get device calibration status"""
    return DeviceController.get_device_calibration(db, str(current_user.id), device_id)

@router.post("/{device_id}/calibrate")
def calibrate_device(
    device_id: str,
    calibration_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calibrate device sensors"""
    return DeviceController.calibrate_device(db, str(current_user.id), device_id, calibration_data) 