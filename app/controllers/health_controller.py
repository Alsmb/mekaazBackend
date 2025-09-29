from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from app.models.vitals import Vital, VitalAggregate
from app.models.device import Device
from app.services.redis_service import redis_service
from app.services.health_analysis_service import HealthAnalysisService
import uuid

class HealthController:
    @staticmethod
    def ingest_vital_data(db: Session, user_id: str, vital_data: dict):
        """Ingest vital data from device (called every 2 seconds)"""
        
        # Validate device connection
        device = db.query(Device).filter(
            Device.device_id == vital_data['device_id'],
            Device.user_id == user_id,
            Device.is_connected == True
        ).first()
        
        if not device:
            raise HTTPException(status_code=400, detail="Device not connected or not found")
        
        # Analyze health condition
        health_condition, is_anomaly = HealthAnalysisService.analyze_vital_signs(vital_data)
        
        # Create vital record
        vital = Vital(
            id=str(uuid.uuid4()),
            user_id=user_id,
            device_id=str(device.id),
            heart_rate=vital_data.get('heart_rate'),
            spo2=vital_data.get('spo2'),
            temperature=vital_data.get('temperature'),
            steps=vital_data.get('steps'),
            blood_pressure_systolic=vital_data.get('blood_pressure_systolic'),
            blood_pressure_diastolic=vital_data.get('blood_pressure_diastolic'),
            respiratory_rate=vital_data.get('respiratory_rate'),
            health_condition=health_condition,
            is_anomaly=is_anomaly,
            timestamp=datetime.utcnow()
        )
        
        db.add(vital)
        db.commit()
        db.refresh(vital)
        
        # Store in Redis for real-time access
        live_data = {
            'heart_rate': vital.heart_rate,
            'spo2': vital.spo2,
            'temperature': vital.temperature,
            'steps': vital.steps,
            'health_condition': vital.health_condition,
            'is_anomaly': vital.is_anomaly
        }
        redis_service.store_live_vital(user_id, live_data)
        
        # Publish to WebSocket subscribers
        redis_service.publish_vital_update(user_id, live_data)
        
        # Check for alerts
        if HealthAnalysisService.should_trigger_alert(health_condition, is_anomaly):
            # TODO: Trigger alert notification
            pass
        
        return vital.to_dict()
    
    @staticmethod
    def get_live_vital(user_id: str):
        """Get latest vital data from Redis"""
        live_data = redis_service.get_live_vital(user_id)
        if not live_data:
            return None
        return live_data
    
    @staticmethod
    def get_vital_history(db: Session, user_id: str, start_time: datetime = None, end_time: datetime = None, limit: int = 100):
        """Get historical vital data"""
        query = db.query(Vital).filter(Vital.user_id == user_id)
        
        if start_time:
            query = query.filter(Vital.timestamp >= start_time)
        if end_time:
            query = query.filter(Vital.timestamp <= end_time)
        
        vitals = query.order_by(Vital.timestamp.desc()).limit(limit).all()
        return [vital.to_dict() for vital in vitals]
    
    @staticmethod
    def get_chart_data(db: Session, user_id: str, period: str = "hour"):
        """Get aggregated chart data for specified period"""
        
        # Try to get from Redis cache first
        cached_data = redis_service.get_vital_aggregate(user_id, period)
        if cached_data:
            return cached_data
        
        # Calculate time range
        now = datetime.utcnow()
        if period == "hour":
            start_time = now - timedelta(hours=1)
        elif period == "day":
            start_time = now - timedelta(days=1)
        elif period == "week":
            start_time = now - timedelta(weeks=1)
        else:
            raise HTTPException(status_code=400, detail="Invalid period")
        
        # Get aggregated data from database
        vitals = db.query(Vital).filter(
            Vital.user_id == user_id,
            Vital.timestamp >= start_time,
            Vital.timestamp <= now
        ).all()
        
        if not vitals:
            return {"period": period, "data": []}
        
        # Calculate aggregates
        heart_rates = [v.heart_rate for v in vitals if v.heart_rate]
        spo2_values = [v.spo2 for v in vitals if v.spo2]
        temperatures = [v.temperature for v in vitals if v.temperature]
        steps_total = sum([v.steps for v in vitals if v.steps])
        anomaly_count = sum([1 for v in vitals if v.is_anomaly])
        
        aggregate_data = {
            "period": period,
            "heart_rate_avg": sum(heart_rates) / len(heart_rates) if heart_rates else None,
            "heart_rate_min": min(heart_rates) if heart_rates else None,
            "heart_rate_max": max(heart_rates) if heart_rates else None,
            "spo2_avg": sum(spo2_values) / len(spo2_values) if spo2_values else None,
            "spo2_min": min(spo2_values) if spo2_values else None,
            "spo2_max": max(spo2_values) if spo2_values else None,
            "temperature_avg": sum(temperatures) / len(temperatures) if temperatures else None,
            "temperature_min": min(temperatures) if temperatures else None,
            "temperature_max": max(temperatures) if temperatures else None,
            "steps_total": steps_total,
            "anomaly_count": anomaly_count,
            "start_time": start_time.isoformat() if start_time else None,
            "end_time": now.isoformat() if now else None
        }
        
        # Cache the result
        redis_service.store_vital_aggregate(user_id, period, aggregate_data)
        
        return aggregate_data
    
    @staticmethod
    def get_history(user_id: str, db: Session):
        """Get vitals history for user"""
        return HealthController.get_vital_history(db, user_id)
    
    @staticmethod
    def get_live(user_id: str, db: Session):
        """Get live vitals for user"""
        return HealthController.get_live_vital(user_id) 

    @staticmethod
    def calculate_health_score(db: Session, user_id: str):
        """Calculate health score (0-100) based on vital trends"""
        # Get recent vitals
        recent_vitals = db.query(Vital).filter_by(user_id=user_id).order_by(Vital.timestamp.desc()).limit(10).all()
        
        if not recent_vitals:
            return {"score": 0, "status": "No data", "message": "No vital data available"}
        
        # Calculate score based on vital ranges
        heart_rate_score = 0
        spo2_score = 0
        temperature_score = 0
        
        for vital in recent_vitals:
            # Heart rate scoring (60-100 is good)
            if 60 <= vital.heart_rate <= 100:
                heart_rate_score += 10
            elif 50 <= vital.heart_rate <= 110:
                heart_rate_score += 5
            
            # SpO2 scoring (95-100 is good)
            if 95 <= vital.spo2 <= 100:
                spo2_score += 10
            elif 90 <= vital.spo2 <= 95:
                spo2_score += 5
            
            # Temperature scoring (36-37.5 is good)
            if 36.0 <= vital.temperature <= 37.5:
                temperature_score += 10
            elif 35.5 <= vital.temperature <= 38.0:
                temperature_score += 5
        
        # Average scores
        avg_heart_rate = heart_rate_score / len(recent_vitals)
        avg_spo2 = spo2_score / len(recent_vitals)
        avg_temperature = temperature_score / len(recent_vitals)
        
        # Calculate overall score
        total_score = min(100, (avg_heart_rate + avg_spo2 + avg_temperature) * 3.33)
        
        # Determine status
        if total_score >= 80:
            status = "Excellent"
        elif total_score >= 60:
            status = "Good"
        elif total_score >= 40:
            status = "Fair"
        else:
            status = "Poor"
        
        return {
            "score": int(total_score),
            "status": status,
            "message": f"Based on {len(recent_vitals)} recent readings"
        }

    @staticmethod
    def get_health_trends(db: Session, user_id: str, metric: str, period: str):
        """Get health trends for specific metric over time period"""
        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        
        if period == "day":
            start_time = now - timedelta(days=1)
        elif period == "week":
            start_time = now - timedelta(weeks=1)
        elif period == "month":
            start_time = now - timedelta(days=30)
        else:
            start_time = now - timedelta(weeks=1)
        
        # Get vitals for the period
        vitals = db.query(Vital).filter(
            Vital.user_id == user_id,
            Vital.timestamp >= start_time
        ).order_by(Vital.timestamp.asc()).all()
        
        # Extract metric data
        data_points = []
        for vital in vitals:
            if metric == "heart_rate" and vital.heart_rate:
                data_points.append({"timestamp": vital.timestamp.isoformat(), "value": vital.heart_rate})
            elif metric == "spo2" and vital.spo2:
                data_points.append({"timestamp": vital.timestamp.isoformat(), "value": vital.spo2})
            elif metric == "temperature" and vital.temperature:
                data_points.append({"timestamp": vital.timestamp.isoformat(), "value": vital.temperature})
            elif metric == "steps" and vital.steps:
                data_points.append({"timestamp": vital.timestamp.isoformat(), "value": vital.steps})
        
        # Calculate average
        if data_points:
            avg_value = sum(point["value"] for point in data_points) / len(data_points)
        else:
            avg_value = 0
        
        return {
            "metric": metric,
            "period": period,
            "average": round(avg_value, 2),
            "data_points": data_points,
            "total_points": len(data_points)
        }

    @staticmethod
    def get_health_alerts(db: Session, user_id: str):
        """Get recent health alerts and notifications"""
        from datetime import datetime, timedelta
        
        # Get recent vitals for analysis
        recent_vitals = db.query(Vital).filter_by(user_id=user_id).order_by(Vital.timestamp.desc()).limit(20).all()
        
        alerts = []
        
        for vital in recent_vitals:
            # Heart rate alerts
            if vital.heart_rate and vital.heart_rate > 100:
                alerts.append({
                    "type": "heart_rate_high",
                    "title": "Elevated Heart Rate",
                    "message": f"Heart rate was elevated: {vital.heart_rate} bpm",
                    "value": f"{vital.heart_rate} bpm",
                    "timestamp": vital.timestamp.isoformat(),
                    "severity": "warning"
                })
            elif vital.heart_rate and vital.heart_rate < 60:
                alerts.append({
                    "type": "heart_rate_low",
                    "title": "Low Heart Rate",
                    "message": f"Heart rate was low: {vital.heart_rate} bpm",
                    "value": f"{vital.heart_rate} bpm",
                    "timestamp": vital.timestamp.isoformat(),
                    "severity": "warning"
                })
            
            # SpO2 alerts
            if vital.spo2 and vital.spo2 < 95:
                alerts.append({
                    "type": "spo2_low",
                    "title": "Low Oxygen Saturation",
                    "message": f"SpO2 was below normal: {vital.spo2}%",
                    "value": f"{vital.spo2}%",
                    "timestamp": vital.timestamp.isoformat(),
                    "severity": "critical"
                })
            
            # Temperature alerts
            if vital.temperature and vital.temperature > 37.5:
                alerts.append({
                    "type": "temperature_high",
                    "title": "Elevated Temperature",
                    "message": f"Temperature was elevated: {vital.temperature}°C",
                    "value": f"{vital.temperature}°C",
                    "timestamp": vital.timestamp.isoformat(),
                    "severity": "warning"
                })
        
        return {
            "alerts": alerts[:10],  # Return last 10 alerts
            "total_alerts": len(alerts),
            "unread_count": len(alerts)
        } 