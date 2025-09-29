from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sos import (
    SOSResponse, SOSTriggerRequest, SOSCancelRequest, 
    SOSResolveRequest, SOSHistoryResponse
)
from app.controllers.sos_controller import SOSController

router = APIRouter(prefix="/sos", tags=["SOS"])

@router.post("/trigger", response_model=SOSResponse)
def trigger_sos(
    data: SOSTriggerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trigger SOS emergency alert"""
    sos = SOSController.trigger_sos(db, str(current_user.id), data.dict())
    return sos

@router.post("/cancel", response_model=SOSResponse)
def cancel_sos(
    data: SOSCancelRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel active SOS alert"""
    # Get active SOS for user
    active_sos = SOSController.get_active_sos(db, str(current_user.id))
    if isinstance(active_sos, dict):
        sos_id = active_sos["id"]
    else:
        sos_id = str(active_sos.id)
    sos = SOSController.cancel_sos(db, str(current_user.id), sos_id, data.reason)
    return sos

@router.post("/{sos_id}/resolve", response_model=SOSResponse)
def resolve_sos(
    sos_id: str,
    data: SOSResolveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resolve SOS alert (for family members or emergency contacts)"""
    sos = SOSController.resolve_sos(db, sos_id, data.resolved_by, data.resolution_notes)
    return sos

@router.get("/history", response_model=SOSHistoryResponse)
def get_sos_history(
    limit: int = Query(50, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get SOS history for user"""
    sos_alerts = SOSController.get_sos_history(db, str(current_user.id), limit)
    return {
        "sos_alerts": sos_alerts,
        "total_count": len(sos_alerts)
    }

@router.get("/active", response_model=SOSResponse)
def get_active_sos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active SOS alert for user"""
    sos = SOSController.get_active_sos(db, str(current_user.id))
    return sos

@router.get("/{sos_id}/notifications")
def get_sos_notifications(
    sos_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications sent for a specific SOS alert"""
    notifications = SOSController.get_sos_notifications(db, sos_id)
    return notifications 