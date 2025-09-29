from typing import Dict, Any, Tuple
from datetime import datetime

class HealthAnalysisService:
    # Health condition thresholds
    HEART_RATE_NORMAL = (60, 100)
    HEART_RATE_WARNING = (50, 120)
    SPO2_NORMAL = (95, 100)
    SPO2_WARNING = (90, 95)
    TEMPERATURE_NORMAL = (36.1, 37.2)
    TEMPERATURE_WARNING = (35.5, 38.0)
    BLOOD_PRESSURE_SYSTOLIC_NORMAL = (90, 140)
    BLOOD_PRESSURE_DIASTOLIC_NORMAL = (60, 90)
    RESPIRATORY_RATE_NORMAL = (12, 20)
    
    @staticmethod
    def analyze_vital_signs(vital_data: Dict[str, Any]) -> Tuple[str, bool]:
        """
        Analyze vital signs and return health condition and anomaly flag
        Returns: (health_condition, is_anomaly)
        """
        anomalies = []
        health_condition = "normal"
        
        # Heart Rate Analysis
        if vital_data.get('heart_rate'):
            hr = vital_data['heart_rate']
            if hr < HealthAnalysisService.HEART_RATE_NORMAL[0] or hr > HealthAnalysisService.HEART_RATE_NORMAL[1]:
                anomalies.append("heart_rate")
                if hr < HealthAnalysisService.HEART_RATE_WARNING[0] or hr > HealthAnalysisService.HEART_RATE_WARNING[1]:
                    health_condition = "critical"
                elif health_condition == "normal":
                    health_condition = "warning"
        
        # SpO2 Analysis
        if vital_data.get('spo2'):
            spo2 = vital_data['spo2']
            if spo2 < HealthAnalysisService.SPO2_NORMAL[0]:
                anomalies.append("spo2")
                if spo2 < HealthAnalysisService.SPO2_WARNING[0]:
                    health_condition = "critical"
                elif health_condition == "normal":
                    health_condition = "warning"
        
        # Temperature Analysis
        if vital_data.get('temperature'):
            temp = vital_data['temperature']
            if temp < HealthAnalysisService.TEMPERATURE_NORMAL[0] or temp > HealthAnalysisService.TEMPERATURE_NORMAL[1]:
                anomalies.append("temperature")
                if temp < HealthAnalysisService.TEMPERATURE_WARNING[0] or temp > HealthAnalysisService.TEMPERATURE_WARNING[1]:
                    health_condition = "critical"
                elif health_condition == "normal":
                    health_condition = "warning"
        
        # Blood Pressure Analysis
        if vital_data.get('blood_pressure_systolic') and vital_data.get('blood_pressure_diastolic'):
            systolic = vital_data['blood_pressure_systolic']
            diastolic = vital_data['blood_pressure_diastolic']
            
            if (systolic < HealthAnalysisService.BLOOD_PRESSURE_SYSTOLIC_NORMAL[0] or 
                systolic > HealthAnalysisService.BLOOD_PRESSURE_SYSTOLIC_NORMAL[1] or
                diastolic < HealthAnalysisService.BLOOD_PRESSURE_DIASTOLIC_NORMAL[0] or
                diastolic > HealthAnalysisService.BLOOD_PRESSURE_DIASTOLIC_NORMAL[1]):
                anomalies.append("blood_pressure")
                if health_condition == "normal":
                    health_condition = "warning"
        
        # Respiratory Rate Analysis
        if vital_data.get('respiratory_rate'):
            rr = vital_data['respiratory_rate']
            if rr < HealthAnalysisService.RESPIRATORY_RATE_NORMAL[0] or rr > HealthAnalysisService.RESPIRATORY_RATE_NORMAL[1]:
                anomalies.append("respiratory_rate")
                if health_condition == "normal":
                    health_condition = "warning"
        
        is_anomaly = len(anomalies) > 0
        
        return health_condition, is_anomaly
    
    @staticmethod
    def should_trigger_alert(health_condition: str, is_anomaly: bool) -> bool:
        """Determine if an alert should be triggered"""
        return health_condition in ["warning", "critical"] or is_anomaly
    
    @staticmethod
    def get_alert_message(anomalies: list, health_condition: str) -> str:
        """Generate alert message based on anomalies"""
        if health_condition == "critical":
            return f"CRITICAL: Multiple vital signs outside normal range: {', '.join(anomalies)}"
        elif health_condition == "warning":
            return f"WARNING: Some vital signs need attention: {', '.join(anomalies)}"
        else:
            return "All vital signs are normal" 