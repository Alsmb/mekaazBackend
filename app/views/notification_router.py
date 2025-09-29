from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.controllers.notification_controller import NotificationController
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications with badges"""
    return NotificationController.get_user_notifications(db, str(current_user.id))

@router.post("/mark-read")
def mark_notifications_read(
    notification_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notifications as read"""
    return NotificationController.mark_notifications_read(db, str(current_user.id), notification_ids)

@router.get("/settings")
def get_notification_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notification settings"""
    return NotificationController.get_notification_settings(db, str(current_user.id))

@router.patch("/settings")
def update_notification_settings(
    settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user notification settings"""
    return NotificationController.update_notification_settings(db, str(current_user.id), settings)

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    return NotificationController.get_unread_count(db, str(current_user.id))

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific notification"""
    return NotificationController.delete_notification(db, str(current_user.id), notification_id)

@router.post("/create")
def create_notification(
    notification_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new notification (for testing)"""
    return NotificationController.create_notification(db, str(current_user.id), notification_data) 