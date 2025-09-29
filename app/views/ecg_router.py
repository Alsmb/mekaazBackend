from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.ecg import (
    ECGResponse, ECGStartRequest, ECGDataRequest, ECGCompleteRequest,
    ECGDownloadResponse, ECGAnalysisResponse
)
from app.controllers.ecg_controller import ECGController

router = APIRouter(prefix="/ecg", tags=["ECG"])

@router.post("/start", response_model=ECGResponse)
def start_ecg_recording(
    data: ECGStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new ECG recording session"""
    ecg = ECGController.start_ecg_recording(db, str(current_user.id), data.device_id, data.dict())
    return ecg

@router.get("/history", response_model=list[ECGResponse])
def get_ecg_history(
    limit: int = Query(50, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ECG recording history for user"""
    ecg_recordings = ECGController.get_ecg_history(db, str(current_user.id), limit)
    return ecg_recordings

@router.post("/{ecg_id}/data", response_model=ECGResponse)
def update_ecg_data(
    ecg_id: str,
    data: ECGDataRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update ECG recording with data from device"""
    ecg = ECGController.update_ecg_data(db, ecg_id, data.ecg_data)
    return ecg

@router.post("/{ecg_id}/complete", response_model=ECGResponse)
def complete_ecg_recording(
    ecg_id: str,
    data: ECGCompleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete ECG recording and start processing"""
    ecg = ECGController.complete_ecg_recording(db, ecg_id, data.final_data)
    return ecg

@router.get("/{ecg_id}", response_model=ECGResponse)
def get_ecg_recording(
    ecg_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ECG recording by ID"""
    ecg = ECGController.get_ecg_recording(db, ecg_id, str(current_user.id))
    return ecg

@router.get("/{ecg_id}/download", response_model=ECGDownloadResponse)
def download_ecg_pdf(
    ecg_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get download URL for ECG PDF"""
    download_info = ECGController.download_ecg_pdf(db, ecg_id, str(current_user.id))
    return download_info

@router.get("/{ecg_id}/analyze", response_model=ECGAnalysisResponse)
def analyze_ecg_data(
    ecg_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze ECG data and return health metrics"""
    analysis = ECGController.analyze_ecg_data(db, ecg_id, str(current_user.id))
    return analysis 