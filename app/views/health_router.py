from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.vitals import VitalResponse, VitalIngestRequest, VitalHistoryRequest, ChartDataResponse, LiveVitalResponse
from app.controllers.health_controller import HealthController

router = APIRouter(prefix="/vitals", tags=["Health"])

@router.post("/ingest", response_model=VitalResponse)
def ingest_vital_data(
    data: VitalIngestRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ingest vital data from connected device (called every 2 seconds)"""
    return HealthController.ingest_vital_data(db, str(current_user.id), data.dict())

@router.get("/history", response_model=list[VitalResponse])
def get_history(
    start_time: str = Query(None, description="Start time (ISO format)"),
    end_time: str = Query(None, description="End time (ISO format)"),
    limit: int = Query(100, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get vitals history with optional time filtering"""
    from datetime import datetime

    start_dt = datetime.fromisoformat(start_time) if start_time else None
    end_dt = datetime.fromisoformat(end_time) if end_time else None

    return HealthController.get_vital_history(
        db,
        str(current_user.id),
        start_dt,
        end_dt,
        limit
    )

@router.get("/live", response_model=LiveVitalResponse)
def get_live_vital(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get latest live vital data"""
    live_data = HealthController.get_live_vital(str(current_user.id))
    if not live_data:
        raise HTTPException(status_code=404, detail="No live vital data available")
    return live_data

@router.get("/charts/{period}", response_model=ChartDataResponse)
def get_chart_data(
    period: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get aggregated chart data for specified period"""
    if period not in ["hour", "day", "week"]:
        raise HTTPException(status_code=400, detail="Invalid period. Use: hour, day, or week")

    data = HealthController.get_chart_data(db, str(current_user.id), period)
    return ChartDataResponse(period=period, data=[data])

# NEW ENDPOINTS FOR FRONTEND COMPATIBILITY

@router.get("/health-score")
def get_health_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get calculated health score (0-100) based on vital trends"""
    return HealthController.calculate_health_score(db, str(current_user.id))

@router.get("/trends/{metric}")
def get_health_trends(
    metric: str,
    period: str = Query("week", description="Time period: day, week, month"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health trends for specific metric over time period"""
    if metric not in ["heart_rate", "spo2", "temperature", "steps"]:
        raise HTTPException(status_code=400, detail="Invalid metric")

    return HealthController.get_health_trends(db, str(current_user.id), metric, period)

@router.get("/alerts")
def get_health_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent health alerts and notifications"""
    return HealthController.get_health_alerts(db, str(current_user.id)) 