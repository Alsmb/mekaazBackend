from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sos import SOS, SOSNotification
from app.models.user import User
from app.services.emergency_service import EmergencyService
from app.services.redis_service import redis_service
import json
import uuid

class SOSController:
    @staticmethod
    def trigger_sos(db: Session, user_id: str, sos_data: dict) -> SOS:
        """Trigger SOS emergency alert"""

        # Check if user already has an active SOS
        active_sos = db.query(SOS).filter(
            SOS.user_id == user_id,
            SOS.status == "active"
        ).first()

        if active_sos:
            raise HTTPException(status_code=400, detail="Active SOS alert already exists")

        # Get current vital data from Redis
        live_vitals = redis_service.get_live_vital(user_id)
        if live_vitals:
            sos_data["vital_data"] = json.dumps(live_vitals)

        # Trigger SOS through emergency service
        sos = EmergencyService.trigger_sos(db, user_id, sos_data)

        return sos.to_dict()

    @staticmethod
    def cancel_sos(db: Session, user_id: str, sos_id: str, reason: str = None) -> SOS:
        """Cancel active SOS alert"""

        try:
            sos = EmergencyService.cancel_sos(db, sos_id, user_id, reason)
            return sos.to_dict()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def resolve_sos(db: Session, sos_id: str, resolved_by: str, resolution_notes: str = None) -> SOS:
        """Resolve SOS alert (for family members or emergency contacts)"""
        
        try:
            # If resolved_by is not a UUID, treat it as a description and use the current user
            if not resolved_by or len(resolved_by) != 36:  # UUID length check
                # For now, we'll use a default user ID or handle it differently
                resolved_by = "b804b8fe-42e2-433e-8d31-069b2c322aad"  # Default user ID
            
            sos = EmergencyService.resolve_sos(db, sos_id, resolved_by, resolution_notes)
            return sos.to_dict()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def get_sos_history(db: Session, user_id: str, limit: int = 50) -> list:
        """Get SOS history for user"""

        sos_alerts = EmergencyService.get_sos_history(db, user_id, limit)
        return [sos.to_dict() for sos in sos_alerts]

    @staticmethod
    def get_active_sos(db: Session, user_id: str) -> SOS:
        """Get active SOS alert for user"""

        active_sos = db.query(SOS).filter(
            SOS.user_id == user_id,
            SOS.status == "active"
        ).first()

        if not active_sos:
            raise HTTPException(status_code=404, detail="No active SOS alert found")

        return active_sos.to_dict()

    @staticmethod
    def get_sos_notifications(db: Session, sos_id: str) -> list:
        """Get notifications sent for a specific SOS alert"""

        notifications = db.query(SOSNotification).filter_by(sos_id=sos_id).all()
        return [notification.to_dict() for notification in notifications] 