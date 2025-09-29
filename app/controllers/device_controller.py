from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.device import Device
from app.models.user import User
import uuid

class DeviceController:
    @staticmethod
    def get_available_devices(db: Session, user_id: str):
        """Get list of available devices for user"""
        devices = db.query(Device).filter_by(user_id=user_id).all()
        return [device.to_dict() for device in devices]
    
    @staticmethod
    def connect_device(db: Session, user_id: str, device_id: str, device_type: str, device_name: str = None):
        """Connect a device to user"""
        
        # Check if device already exists
        existing_device = db.query(Device).filter_by(device_id=device_id).first()
        if existing_device:
            raise HTTPException(status_code=400, detail="Device already connected")
        
        # Create new device
        device = Device(
            id=str(uuid.uuid4()),
            user_id=user_id,
            device_type=device_type,
            device_id=device_id,
            device_name=device_name or f"{device_type}_device",
            is_connected=True,
            last_connected=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        
        db.add(device)
        db.commit()
        db.refresh(device)
        
        return device.to_dict()
    
    @staticmethod
    def disconnect_device(db: Session, user_id: str, device_id: str):
        """Disconnect a device"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        device.is_connected = False
        db.commit()
        
        return {"message": "Device disconnected successfully"}
    
    @staticmethod
    def get_device_status(db: Session, user_id: str, device_id: str):
        """Get device connection status"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        return device.to_dict() 

    @staticmethod
    def discover_bluetooth_devices():
        """Discover nearby Bluetooth devices (simulated for demo)"""
        # In a real implementation, this would use Bluetooth APIs
        # For demo purposes, return simulated devices
        return [
            {
                "device_id": "Mekaaz-1001",
                "device_name": "Mekaaz-1001",
                "device_type": "heart_monitor",
                "signal_strength": 88,
                "battery_level": 85,
                "is_available": True
            },
            {
                "device_id": "Mekaaz-1002", 
                "device_name": "Mekaaz-1002",
                "device_type": "ecg_device",
                "signal_strength": 72,
                "battery_level": 92,
                "is_available": True
            },
            {
                "device_id": "Mekaaz-1003",
                "device_name": "Mekaaz-1003", 
                "device_type": "heart_monitor",
                "signal_strength": 90,
                "battery_level": 78,
                "is_available": True
            }
        ]

    @staticmethod
    def get_signal_strength(device_id: str):
        """Get signal strength for a specific device"""
        # Simulate signal strength based on device ID
        import random
        base_strength = 70 + (hash(device_id) % 30)  # 70-100 range
        current_strength = max(50, min(100, base_strength + random.randint(-10, 10)))
        
        return {
            "device_id": device_id,
            "signal_strength": current_strength,
            "signal_quality": "Good" if current_strength >= 80 else "Fair" if current_strength >= 60 else "Poor",
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_battery_level(device_id: str):
        """Get battery level for a specific device"""
        # Simulate battery level based on device ID
        import random
        base_level = 80 + (hash(device_id) % 20)  # 80-100 range
        current_level = max(10, min(100, base_level + random.randint(-20, 10)))
        
        return {
            "device_id": device_id,
            "battery_level": current_level,
            "battery_status": "Charging" if current_level < 20 else "Good" if current_level >= 50 else "Low",
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def pair_bluetooth_device(db: Session, user_id: str, device_id: str):
        """Pair with a discovered Bluetooth device"""
        # Check if device is already connected
        existing_device = db.query(Device).filter_by(device_id=device_id).first()
        if existing_device:
            raise HTTPException(status_code=400, detail="Device already connected")
        
        # Get device info from discovery
        discovered_devices = DeviceController.discover_bluetooth_devices()
        device_info = next((d for d in discovered_devices if d["device_id"] == device_id), None)
        
        if not device_info:
            raise HTTPException(status_code=404, detail="Device not found in discovery")
        
        # Create new device connection
        device = Device(
            user_id=user_id,
            device_type=device_info["device_type"],
            device_id=device_id,
            device_name=device_info["device_name"],
            is_connected=True,
            last_connected=datetime.utcnow()
        )
        
        db.add(device)
        db.commit()
        db.refresh(device)
        
        return {
            "message": "Device paired successfully",
            "device": device.to_dict(),
            "signal_strength": device_info["signal_strength"],
            "battery_level": device_info["battery_level"]
        } 

    @staticmethod
    def get_device_firmware(db: Session, user_id: str, device_id: str):
        """Get device firmware information"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Simulate firmware info
        return {
            "device_id": device_id,
            "current_version": "1.2.3",
            "latest_version": "1.2.4",
            "update_available": True,
            "last_check": datetime.utcnow().isoformat(),
            "firmware_size": "2.5 MB",
            "update_notes": "Bug fixes and performance improvements"
        }

    @staticmethod
    def update_device_firmware(db: Session, user_id: str, device_id: str, update_data: dict):
        """Update device firmware"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Simulate firmware update
        return {
            "message": "Firmware update initiated successfully",
            "device_id": device_id,
            "update_status": "in_progress",
            "estimated_time": "5 minutes",
            "progress": 0,
            "update_id": str(uuid.uuid4())
        }

    @staticmethod
    def get_device_calibration(db: Session, user_id: str, device_id: str):
        """Get device calibration status"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Simulate calibration status
        return {
            "device_id": device_id,
            "calibration_status": "calibrated",
            "last_calibration": (datetime.utcnow() - timedelta(days=30)).isoformat(),
            "next_calibration_due": (datetime.utcnow() + timedelta(days=335)).isoformat(),
            "calibration_accuracy": 98.5,
            "sensors": {
                "heart_rate": {"status": "calibrated", "accuracy": 99.2},
                "spo2": {"status": "calibrated", "accuracy": 97.8},
                "temperature": {"status": "calibrated", "accuracy": 98.1}
            }
        }

    @staticmethod
    def calibrate_device(db: Session, user_id: str, device_id: str, calibration_data: dict):
        """Calibrate device sensors"""
        device = db.query(Device).filter(
            Device.user_id == user_id,
            Device.device_id == device_id
        ).first()
        
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        # Simulate calibration process
        return {
            "message": "Device calibration completed successfully",
            "device_id": device_id,
            "calibration_status": "calibrated",
            "calibration_timestamp": datetime.utcnow().isoformat(),
            "calibration_accuracy": 98.5,
            "calibrated_sensors": calibration_data.get("sensors", ["heart_rate", "spo2", "temperature"])
        } 