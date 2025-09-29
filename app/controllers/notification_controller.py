from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification
from app.models.user import User

class NotificationController:
    @staticmethod
    def get_user_notifications(db: Session, user_id: str):
        """Get user notifications with badges"""
        notifications = db.query(Notification).filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(50).all()
        
        return {
            "notifications": [notification.to_dict() for notification in notifications],
            "unread_count": len([n for n in notifications if not n.is_read]),
            "total_count": len(notifications)
        }

    @staticmethod
    def mark_notifications_read(db: Session, user_id: str, notification_ids: list):
        """Mark notifications as read"""
        notifications = db.query(Notification).filter(
            Notification.id.in_(notification_ids),
            Notification.user_id == user_id
        ).all()
        
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": f"Marked {len(notifications)} notifications as read",
            "updated_count": len(notifications)
        }

    @staticmethod
    def get_notification_settings(db: Session, user_id: str):
        """Get user notification settings"""
        # This would typically come from a settings table
        # For now, return default settings
        return {
            "health_alerts": True,
            "family_updates": True,
            "device_alerts": True,
            "emergency_alerts": True,
            "daily_summary": True,
            "weekly_report": True,
            "push_notifications": True,
            "email_notifications": False,
            "sms_notifications": False
        }

    @staticmethod
    def update_notification_settings(db: Session, user_id: str, settings: dict):
        """Update user notification settings"""
        # This would typically save to a settings table
        # For now, just return success
        return {
            "message": "Notification settings updated successfully",
            "settings": settings
        }

    @staticmethod
    def get_unread_count(db: Session, user_id: str):
        """Get count of unread notifications"""
        unread_count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
        
        return {
            "unread_count": unread_count,
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def delete_notification(db: Session, user_id: str, notification_id: int):
        """Delete a specific notification"""
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        db.delete(notification)
        db.commit()
        
        return {
            "message": "Notification deleted successfully",
            "deleted_id": notification_id
        }

    @staticmethod
    def create_notification(db: Session, user_id: str, notification_data: dict):
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=notification_data.get("title"),
            message=notification_data.get("message"),
            notification_type=notification_data.get("type", "general"),
            severity=notification_data.get("severity", "info"),
            is_read=False,
            created_at=datetime.utcnow()
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return notification.to_dict() 