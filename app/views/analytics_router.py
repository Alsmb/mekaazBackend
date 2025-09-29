from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.controllers.analytics_controller import AnalyticsController

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/health-insights")
def get_health_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized health insights and recommendations"""
    return AnalyticsController.get_health_insights(db, str(current_user.id))

@router.get("/anomaly-detection")
def detect_anomalies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect health anomalies and generate alerts"""
    return AnalyticsController.detect_anomalies(db, str(current_user.id))

@router.post("/custom-alerts")
def create_custom_alert(
    alert_config: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create custom health alerts"""
    return AnalyticsController.create_custom_alert(db, str(current_user.id), alert_config)

@router.get("/health-patterns")
def analyze_health_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze health patterns over time"""
    return AnalyticsController.analyze_health_patterns(db, str(current_user.id))

@router.get("/predictive-health")
def get_predictive_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get predictive health insights"""
    return AnalyticsController.get_predictive_health(db, str(current_user.id))

@router.get("/health-comparison")
def compare_health_data(
    period: str = "week",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare health data across different periods"""
    return AnalyticsController.compare_health_data(db, str(current_user.id), period) 