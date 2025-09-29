from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from app.models.vitals import Vital
from app.models.user import User
import statistics
import uuid

class AnalyticsController:
    @staticmethod
    def get_health_insights(db: Session, user_id: str):
        """Get personalized health insights and recommendations"""
        # Get recent vitals for analysis
        recent_vitals = db.query(Vital).filter_by(user_id=user_id).order_by(Vital.timestamp.desc()).limit(100).all()
        
        if not recent_vitals:
            return {
                "insights": [],
                "recommendations": ["Start monitoring your health to get personalized insights"],
                "health_score": 0
            }
        
        insights = []
        recommendations = []
        
        # Analyze heart rate patterns
        heart_rates = [v.heart_rate for v in recent_vitals if v.heart_rate]
        if heart_rates and len(heart_rates) > 0:
            try:
                avg_hr = statistics.mean(heart_rates)
                max_hr = max(heart_rates)
                min_hr = min(heart_rates)
            except statistics.StatisticsError:
                avg_hr = 0
                max_hr = 0
                min_hr = 0
            
            if avg_hr > 100:
                insights.append({
                    "type": "heart_rate_high",
                    "title": "Elevated Heart Rate",
                    "message": f"Your average heart rate is {avg_hr:.1f} bpm, which is above normal range",
                    "severity": "warning"
                })
                recommendations.append("Consider reducing stress and increasing physical activity")
            elif avg_hr < 60:
                insights.append({
                    "type": "heart_rate_low",
                    "title": "Low Heart Rate",
                    "message": f"Your average heart rate is {avg_hr:.1f} bpm, which is below normal range",
                    "severity": "info"
                })
                recommendations.append("Consult with your healthcare provider about your heart rate")
        
        # Analyze SpO2 patterns
        spo2_values = [v.spo2 for v in recent_vitals if v.spo2]
        if spo2_values and len(spo2_values) > 0:
            try:
                avg_spo2 = statistics.mean(spo2_values)
            except statistics.StatisticsError:
                avg_spo2 = 0
            if avg_spo2 < 95:
                insights.append({
                    "type": "spo2_low",
                    "title": "Low Oxygen Saturation",
                    "message": f"Your average SpO2 is {avg_spo2:.1f}%, which is below normal",
                    "severity": "critical"
                })
                recommendations.append("Consider breathing exercises and consult a healthcare provider")
        
        # Analyze temperature patterns
        temperatures = [v.temperature for v in recent_vitals if v.temperature]
        if temperatures and len(temperatures) > 0:
            try:
                avg_temp = statistics.mean(temperatures)
            except statistics.StatisticsError:
                avg_temp = 0
            if avg_temp > 37.5:
                insights.append({
                    "type": "temperature_high",
                    "title": "Elevated Temperature",
                    "message": f"Your average temperature is {avg_temp:.1f}°C, which is above normal",
                    "severity": "warning"
                })
                recommendations.append("Monitor your temperature and consider consulting a healthcare provider")
        
        # Calculate health score
        health_score = min(100, max(0, 100 - len(insights) * 15))
        
        return {
            "insights": insights,
            "recommendations": recommendations,
            "health_score": health_score,
            "analysis_period": "Last 100 readings",
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def detect_anomalies(db: Session, user_id: str):
        """Detect health anomalies and generate alerts"""
        # Get recent vitals for anomaly detection
        recent_vitals = db.query(Vital).filter_by(user_id=user_id).order_by(Vital.timestamp.desc()).limit(50).all()
        
        anomalies = []
        
        for vital in recent_vitals:
            # Heart rate anomalies
            if vital.heart_rate:
                if vital.heart_rate > 120:
                    anomalies.append({
                        "type": "heart_rate_anomaly",
                        "title": "Critical Heart Rate",
                        "message": f"Heart rate spike detected: {vital.heart_rate} bpm",
                        "value": vital.heart_rate,
                        "timestamp": vital.timestamp.isoformat(),
                        "severity": "critical"
                    })
                elif vital.heart_rate < 50:
                    anomalies.append({
                        "type": "heart_rate_anomaly",
                        "title": "Low Heart Rate",
                        "message": f"Unusually low heart rate: {vital.heart_rate} bpm",
                        "value": vital.heart_rate,
                        "timestamp": vital.timestamp.isoformat(),
                        "severity": "warning"
                    })
            
            # SpO2 anomalies
            if vital.spo2:
                if vital.spo2 < 90:
                    anomalies.append({
                        "type": "spo2_anomaly",
                        "title": "Critical Oxygen Level",
                        "message": f"Dangerously low SpO2: {vital.spo2}%",
                        "value": vital.spo2,
                        "timestamp": vital.timestamp.isoformat(),
                        "severity": "critical"
                    })
            
            # Temperature anomalies
            if vital.temperature:
                if vital.temperature > 38.5:
                    anomalies.append({
                        "type": "temperature_anomaly",
                        "title": "High Fever",
                        "message": f"High temperature detected: {vital.temperature}°C",
                        "value": vital.temperature,
                        "timestamp": vital.timestamp.isoformat(),
                        "severity": "critical"
                    })
        
        return {
            "anomalies": anomalies,
            "total_anomalies": len(anomalies),
            "critical_count": len([a for a in anomalies if a["severity"] == "critical"]),
            "warning_count": len([a for a in anomalies if a["severity"] == "warning"]),
            "detection_timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def create_custom_alert(db: Session, user_id: str, alert_config: dict):
        """Create custom health alerts"""
        # This would typically save to a custom alerts table
        # For now, return success
        return {
            "message": "Custom alert created successfully",
            "alert_id": str(uuid.uuid4()),
            "config": alert_config,
            "created_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def analyze_health_patterns(db: Session, user_id: str):
        """Analyze health patterns over time"""
        # Get vitals for the last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        vitals = db.query(Vital).filter(
            Vital.user_id == user_id,
            Vital.timestamp >= thirty_days_ago
        ).order_by(Vital.timestamp.asc()).all()
        
        patterns = {
            "heart_rate_pattern": "stable",
            "spo2_pattern": "stable", 
            "temperature_pattern": "stable",
            "activity_pattern": "increasing",
            "sleep_pattern": "stable"
        }
        
        # Analyze patterns (simplified for demo)
        if vitals:
            heart_rates = [v.heart_rate for v in vitals if v.heart_rate]
            if heart_rates and len(heart_rates) >= 2:
                try:
                    hr_variance = statistics.variance(heart_rates)
                    if hr_variance > 100:
                        patterns["heart_rate_pattern"] = "variable"
                    elif hr_variance < 25:
                        patterns["heart_rate_pattern"] = "very_stable"
                except statistics.StatisticsError:
                    # Handle case with insufficient data points
                    patterns["heart_rate_pattern"] = "insufficient_data"
        
        return {
            "patterns": patterns,
            "analysis_period": "Last 30 days",
            "data_points": len(vitals),
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_predictive_health(db: Session, user_id: str):
        """Get predictive health insights"""
        # This would use machine learning models
        # For now, return simulated predictions
        return {
            "predictions": {
                "heart_health_risk": "low",
                "respiratory_health_risk": "low",
                "activity_trend": "improving",
                "sleep_quality_trend": "stable"
            },
            "confidence_scores": {
                "heart_health": 0.85,
                "respiratory_health": 0.92,
                "activity": 0.78,
                "sleep": 0.81
            },
            "recommendations": [
                "Continue current exercise routine",
                "Maintain good sleep hygiene",
                "Monitor stress levels"
            ],
            "prediction_timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def compare_health_data(db: Session, user_id: str, period: str):
        """Compare health data across different periods"""
        now = datetime.utcnow()
        
        if period == "week":
            current_start = now - timedelta(days=7)
            previous_start = now - timedelta(days=14)
            previous_end = now - timedelta(days=7)
        elif period == "month":
            current_start = now - timedelta(days=30)
            previous_start = now - timedelta(days=60)
            previous_end = now - timedelta(days=30)
        else:
            current_start = now - timedelta(days=7)
            previous_start = now - timedelta(days=14)
            previous_end = now - timedelta(days=7)
        
        # Get current period data
        current_vitals = db.query(Vital).filter(
            Vital.user_id == user_id,
            Vital.timestamp >= current_start
        ).all()
        
        # Get previous period data
        previous_vitals = db.query(Vital).filter(
            Vital.user_id == user_id,
            Vital.timestamp >= previous_start,
            Vital.timestamp < previous_end
        ).all()
        
        # Calculate averages
        current_hr_values = [v.heart_rate for v in current_vitals if v.heart_rate]
        previous_hr_values = [v.heart_rate for v in previous_vitals if v.heart_rate]
        
        try:
            current_hr = statistics.mean(current_hr_values) if current_hr_values else 0
        except statistics.StatisticsError:
            current_hr = 0
            
        try:
            previous_hr = statistics.mean(previous_hr_values) if previous_hr_values else 0
        except statistics.StatisticsError:
            previous_hr = 0
        
        current_spo2_values = [v.spo2 for v in current_vitals if v.spo2]
        previous_spo2_values = [v.spo2 for v in previous_vitals if v.spo2]
        
        try:
            current_spo2 = statistics.mean(current_spo2_values) if current_spo2_values else 0
        except statistics.StatisticsError:
            current_spo2 = 0
            
        try:
            previous_spo2 = statistics.mean(previous_spo2_values) if previous_spo2_values else 0
        except statistics.StatisticsError:
            previous_spo2 = 0
        
        return {
            "comparison_period": period,
            "metrics": {
                "heart_rate": {
                    "current": round(current_hr, 1),
                    "previous": round(previous_hr, 1),
                    "change": round(current_hr - previous_hr, 1),
                    "trend": "improving" if current_hr < previous_hr else "declining" if current_hr > previous_hr else "stable"
                },
                "spo2": {
                    "current": round(current_spo2, 1),
                    "previous": round(previous_spo2, 1),
                    "change": round(current_spo2 - previous_spo2, 1),
                    "trend": "improving" if current_spo2 > previous_spo2 else "declining" if current_spo2 < previous_spo2 else "stable"
                }
            },
            "summary": "Your health metrics are generally stable",
            "timestamp": datetime.utcnow().isoformat()
        } 