from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.sos import SOS, SOSNotification
from app.models.emergency_contact import EmergencyContact
from app.models.user import User
from app.services.sms_service import SMSService
from app.services.email_service import EmailService
import json
import uuid

class EmergencyService:
    @staticmethod
    def trigger_sos(db: Session, user_id: str, sos_data: dict) -> SOS:
        """Trigger SOS alert and notify emergency contacts"""
        
        # Create SOS record
        sos = SOS(
            id=str(uuid.uuid4()),
            user_id=user_id,
            status="active",
            emergency_type=sos_data.get("emergency_type", "medical"),
            location_lat=sos_data.get("location_lat"),
            location_lng=sos_data.get("location_lng"),
            location_address=sos_data.get("location_address"),
            vital_data=sos_data.get("vital_data"),
            notes=sos_data.get("notes"),
            triggered_at=datetime.utcnow()
        )
        
        db.add(sos)
        db.commit()
        db.refresh(sos)
        
        # Get emergency contacts
        contacts = db.query(EmergencyContact).filter_by(user_id=user_id).all()
        
        # Send notifications to all contacts
        for contact in contacts:
            EmergencyService.send_sos_notification(db, sos, contact)
        
        return sos
    
    @staticmethod
    def send_sos_notification(db: Session, sos: SOS, contact: EmergencyContact):
        """Send SOS notification to emergency contact"""
        
        # Create notification record
        notification = SOSNotification(
            id=str(uuid.uuid4()),
            sos_id=str(sos.id),
            contact_id=str(contact.id),
            notification_type="sms",  # Default to SMS for emergency
            sent_at=datetime.utcnow()
        )
        
        db.add(notification)
        db.commit()
        
        # Send SMS notification
        message = EmergencyService.create_sos_message(db, sos, contact)
        SMSService.send_emergency_alert(contact.phone, message)
        
        # Update notification as delivered
        notification.delivered = True
        notification.delivered_at = datetime.utcnow()
        db.commit()
    
    @staticmethod
    def create_sos_message(db: Session, sos: SOS, contact: EmergencyContact) -> str:
        """Create emergency message for contact"""
        
        # Get user details from database
        user = db.query(User).filter_by(id=sos.user_id).first()
        user_name = user.name if user else "Unknown User"
        
        message = f"EMERGENCY ALERT: {user_name} has triggered an SOS alert. "
        message += f"Emergency Type: {sos.emergency_type}. "
        
        if sos.location_address:
            message += f"Location: {sos.location_address}. "
        
        if sos.notes:
            message += f"Notes: {sos.notes}. "
        
        message += "Please respond immediately."
        
        return message
    
    @staticmethod
    def cancel_sos(db: Session, sos_id: str, user_id: str, reason: str = None) -> SOS:
        """Cancel active SOS alert"""
        
        sos = db.query(SOS).filter(
            SOS.id == sos_id,
            SOS.user_id == user_id,
            SOS.status == "active"
        ).first()
        
        if not sos:
            raise ValueError("Active SOS alert not found")
        
        sos.status = "cancelled"
        if reason:
            sos.notes = f"Cancelled: {reason}"
        
        db.commit()
        db.refresh(sos)
        
        return sos
    
    @staticmethod
    def resolve_sos(db: Session, sos_id: str, resolved_by: str, resolution_notes: str = None) -> SOS:
        """Resolve SOS alert"""
        
        sos = db.query(SOS).filter(
            SOS.id == sos_id,
            SOS.status == "active"
        ).first()
        
        if not sos:
            raise ValueError("Active SOS alert not found")
        
        sos.status = "resolved"
        sos.resolved_at = datetime.utcnow()
        sos.resolved_by = resolved_by
        
        if resolution_notes:
            sos.notes = f"Resolved: {resolution_notes}"
        
        db.commit()
        db.refresh(sos)
        
        return sos
    
    @staticmethod
    def get_sos_history(db: Session, user_id: str, limit: int = 50) -> List[SOS]:
        """Get SOS history for user"""
        
        sos_alerts = db.query(SOS).filter(
            SOS.user_id == user_id
        ).order_by(SOS.triggered_at.desc()).limit(limit).all()
        
        return sos_alerts 