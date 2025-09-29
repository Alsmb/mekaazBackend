from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.ecg import ECG, ECGSession
from app.models.device import Device
from app.models.user import User
from app.services.ecg_service import ECGService
import json
import uuid

class ECGController:
    @staticmethod
    def start_ecg_recording(db: Session, user_id: str, device_id: str, recording_data: dict) -> ECG:
        """Start a new ECG recording session"""
        # Verify device connection
        device = db.query(Device).filter(
            Device.device_id == device_id,
            Device.user_id == user_id,
            Device.is_connected == True
        ).first()

        if not device:
            raise HTTPException(status_code=400, detail="Device not connected or not found")

        # Create ECG recording
        ecg = ECG(
            id=str(uuid.uuid4()),
            user_id=user_id,
            device_id=str(device.id),
            recording_duration=recording_data.get("recording_duration", "30_seconds"),
            status="recording",
            recording_started_at=datetime.utcnow(),
            created_at=datetime.utcnow()
        )

        db.add(ecg)
        db.commit()
        db.refresh(ecg)

        # Create ECG session
        session = ECGSession(
            id=str(uuid.uuid4()),
            ecg_id=str(ecg.id),
            session_type=recording_data.get("session_type", "single_lead"),
            lead_count=recording_data.get("lead_count", 1),
            sampling_rate=recording_data.get("sampling_rate", 500),
            resolution=recording_data.get("resolution", 12),
            created_at=datetime.utcnow()
        )

        db.add(session)
        db.commit()

        return ecg.to_dict()

    @staticmethod
    def update_ecg_data(db: Session, ecg_id: str, ecg_data: dict) -> ECG:
        """Update ECG recording with data from device"""
        ecg = db.query(ECG).filter_by(id=ecg_id).first()
        if not ecg:
            raise HTTPException(status_code=404, detail="ECG recording not found")

        if ecg.status != "recording":
            raise HTTPException(status_code=400, detail="ECG recording is not active")

        # Update ECG data
        ecg.ecg_data = json.dumps(ecg_data)
        db.commit()
        db.refresh(ecg)

        return ecg.to_dict()

    @staticmethod
    def complete_ecg_recording(db: Session, ecg_id: str, final_data: dict) -> ECG:
        """Complete ECG recording and start processing"""
        ecg = db.query(ECG).filter_by(id=ecg_id).first()
        if not ecg:
            raise HTTPException(status_code=404, detail="ECG recording not found")

        if ecg.status != "recording":
            raise HTTPException(status_code=400, detail="ECG recording is not active")

        # Update with final data
        ecg.ecg_data = json.dumps(final_data)
        ecg.status = "processing"
        ecg.recording_completed_at = datetime.utcnow()
        ecg.processing_started_at = datetime.utcnow()

        db.commit()
        db.refresh(ecg)

        # Start background processing (in production, use Celery)
        ECGController.process_ecg_recording(db, ecg)

        return ecg.to_dict()

    @staticmethod
    def process_ecg_recording(db: Session, ecg: ECG) -> ECG:
        """Process ECG recording and generate PDF"""
        try:
            # Parse ECG data
            ecg_data = json.loads(ecg.ecg_data) if ecg.ecg_data else {}

            # Get user info
            user = db.query(User).filter_by(id=ecg.user_id).first()
            device = db.query(Device).filter_by(id=ecg.device_id).first()

            user_info = {
                "name": user.name if user else "Unknown",
                "device_id": device.device_id if device else "Unknown"
            }

            # Generate PDF
            pdf_bytes = ECGService.generate_ecg_pdf(ecg_data, user_info)

            # In production, upload to S3/Supabase
            # For now, store as base64 in database (not recommended for production)
            import base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode()

            # Update ECG record
            ecg.pdf_url = f"data:application/pdf;base64,{pdf_base64}"
            ecg.status = "completed"
            ecg.processing_completed_at = datetime.utcnow()
            ecg.file_size = len(pdf_bytes)

            db.commit()
            db.refresh(ecg)

            return ecg.to_dict()

        except Exception as e:
            # Update status to failed
            ecg.status = "failed"
            db.commit()
            raise HTTPException(status_code=500, detail=f"ECG processing failed: {str(e)}")

    @staticmethod
    def get_ecg_recording(db: Session, ecg_id: str, user_id: str) -> ECG:
        """Get ECG recording by ID"""
        ecg = db.query(ECG).filter(
            ECG.id == ecg_id,
            ECG.user_id == user_id
        ).first()

        if not ecg:
            raise HTTPException(status_code=404, detail="ECG recording not found")

        return ecg.to_dict()

    @staticmethod
    def get_ecg_history(db: Session, user_id: str, limit: int = 50) -> list:
        """Get ECG recording history for user"""
        ecg_recordings = db.query(ECG).filter(
            ECG.user_id == user_id
        ).order_by(ECG.created_at.desc()).limit(limit).all()

        return [ecg.to_dict() for ecg in ecg_recordings]

    @staticmethod
    def download_ecg_pdf(db: Session, ecg_id: str, user_id: str) -> dict:
        """Get download URL for ECG PDF"""
        ecg = ECGController.get_ecg_recording(db, ecg_id, user_id)

        if ecg["status"] != "completed":
            raise HTTPException(status_code=400, detail="ECG recording not completed")

        if not ecg["pdf_url"]:
            raise HTTPException(status_code=404, detail="PDF not available")

        # In production, generate signed URL for S3/Supabase
        # For now, return the base64 data
        return {
            "download_url": ecg["pdf_url"],
            "expires_at": datetime.utcnow() + timedelta(hours=24),
            "file_size": ecg["file_size"] or 0
        }

    @staticmethod
    def analyze_ecg_data(db: Session, ecg_id: str, user_id: str) -> dict:
        """Analyze ECG data and return health metrics"""
        ecg = ECGController.get_ecg_recording(db, ecg_id, user_id)

        if not ecg["ecg_data"]:
            raise HTTPException(status_code=400, detail="No ECG data available")

        # Parse ECG data
        ecg_data = json.loads(ecg["ecg_data"])

        # Analyze data
        analysis = ECGService.analyze_ecg_data(ecg_data)

        return {
            "ecg_id": str(ecg["id"]),
            "heart_rate": analysis["heart_rate"],
            "rhythm": analysis["rhythm"],
            "abnormalities": analysis["abnormalities"],
            "confidence_score": analysis["confidence_score"],
            "analysis_completed_at": datetime.utcnow()
        } 