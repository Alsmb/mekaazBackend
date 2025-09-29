import json
import os
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
import base64

class ECGService:
    @staticmethod
    def generate_ecg_pdf(ecg_data: Dict[str, Any], user_info: Dict[str, Any]) -> bytes:
        """Generate PDF report from ECG data"""
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("ECG Recording Report", title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information
        story.append(Paragraph("Patient Information", styles['Heading2']))
        patient_info = [
            ["Name:", user_info.get('name', 'N/A')],
            ["Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Recording Duration:", "30 seconds"],
            ["Device ID:", user_info.get('device_id', 'N/A')]
        ]
        
        patient_table = Table(patient_info, colWidths=[100, 300])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # ECG Analysis Results
        story.append(Paragraph("ECG Analysis", styles['Heading2']))
        
        # Extract ECG data
        ecg_readings = ecg_data.get('readings', [])
        if ecg_readings:
            # Calculate basic statistics
            readings = [float(r) for r in ecg_readings if isinstance(r, (int, float))]
            if readings:
                min_val = min(readings)
                max_val = max(readings)
                avg_val = sum(readings) / len(readings)
                
                analysis_data = [
                    ["Parameter", "Value"],
                    ["Minimum Value:", f"{min_val:.2f}"],
                    ["Maximum Value:", f"{max_val:.2f}"],
                    ["Average Value:", f"{avg_val:.2f}"],
                    ["Total Readings:", str(len(readings))],
                    ["Recording Quality:", "Good" if len(readings) > 1000 else "Fair"]
                ]
                
                analysis_table = Table(analysis_data, colWidths=[150, 250])
                analysis_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                    ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
                ]))
                story.append(analysis_table)
        
        story.append(Spacer(1, 20))
        
        # Generate ECG waveform plot
        if ecg_readings:
            try:
                # Create matplotlib plot
                plt.figure(figsize=(10, 4))
                readings = [float(r) for r in ecg_readings[:1000]]  # Limit to first 1000 points
                plt.plot(readings, linewidth=0.5, color='blue')
                plt.title('ECG Waveform')
                plt.xlabel('Time (samples)')
                plt.ylabel('Amplitude')
                plt.grid(True, alpha=0.3)
                
                # Save plot to bytes
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
                img_buffer.seek(0)
                plt.close()
                
                # Convert to base64 for PDF embedding
                img_data = base64.b64encode(img_buffer.getvalue()).decode()
                
                # Add image to PDF (simplified - in production use proper image handling)
                story.append(Paragraph("ECG Waveform", styles['Heading3']))
                story.append(Paragraph(f"<img src='data:image/png;base64,{img_data}' width='500' height='200'/>", styles['Normal']))
                
            except Exception as e:
                story.append(Paragraph(f"Error generating waveform: {str(e)}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    @staticmethod
    def analyze_ecg_data(ecg_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ECG data and return health metrics"""
        
        readings = ecg_data.get('readings', [])
        if not readings:
            return {
                "heart_rate": None,
                "rhythm": "unknown",
                "abnormalities": ["No data available"],
                "confidence_score": 0.0
            }
        
        try:
            # Convert to numeric values
            numeric_readings = [float(r) for r in readings if isinstance(r, (int, float))]
            
            if len(numeric_readings) < 100:
                return {
                    "heart_rate": None,
                    "rhythm": "insufficient_data",
                    "abnormalities": ["Insufficient data for analysis"],
                    "confidence_score": 0.0
                }
            
            # Basic heart rate calculation (simplified)
            # In production, use proper ECG analysis algorithms
            heart_rate = ECGService.calculate_heart_rate(numeric_readings)
            
            # Rhythm analysis
            rhythm = ECGService.analyze_rhythm(numeric_readings, heart_rate)
            
            # Detect abnormalities
            abnormalities = ECGService.detect_abnormalities(numeric_readings, heart_rate)
            
            # Calculate confidence score
            confidence_score = ECGService.calculate_confidence(numeric_readings)
            
            return {
                "heart_rate": heart_rate,
                "rhythm": rhythm,
                "abnormalities": abnormalities,
                "confidence_score": confidence_score
            }
            
        except Exception as e:
            return {
                "heart_rate": None,
                "rhythm": "error",
                "abnormalities": [f"Analysis error: {str(e)}"],
                "confidence_score": 0.0
            }
    
    @staticmethod
    def calculate_heart_rate(readings: List[float]) -> Optional[int]:
        """Calculate heart rate from ECG readings (simplified)"""
        try:
            # Simple peak detection (in production, use proper ECG algorithms)
            threshold = np.mean(readings) + np.std(readings) * 0.5
            peaks = []
            
            for i in range(1, len(readings) - 1):
                if readings[i] > threshold and readings[i] > readings[i-1] and readings[i] > readings[i+1]:
                    peaks.append(i)
            
            if len(peaks) < 2:
                return None
            
            # Calculate intervals between peaks
            intervals = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
            avg_interval = np.mean(intervals)
            
            # Convert to heart rate (assuming 500 Hz sampling rate)
            heart_rate = int(60 * 500 / avg_interval)
            
            return heart_rate if 40 <= heart_rate <= 200 else None
            
        except:
            return None
    
    @staticmethod
    def analyze_rhythm(readings: List[float], heart_rate: Optional[int]) -> str:
        """Analyze heart rhythm"""
        if heart_rate is None:
            return "unknown"
        
        if heart_rate < 60:
            return "bradycardia"
        elif heart_rate > 100:
            return "tachycardia"
        else:
            return "normal"
    
    @staticmethod
    def detect_abnormalities(readings: List[float], heart_rate: Optional[int]) -> List[str]:
        """Detect ECG abnormalities"""
        abnormalities = []
        
        if heart_rate is None:
            abnormalities.append("Unable to calculate heart rate")
        elif heart_rate < 60:
            abnormalities.append("Bradycardia detected")
        elif heart_rate > 100:
            abnormalities.append("Tachycardia detected")
        
        # Check for irregular rhythm (simplified)
        if len(readings) > 1000:
            first_half = readings[:len(readings)//2]
            second_half = readings[len(readings)//2:]
            
            hr1 = ECGService.calculate_heart_rate(first_half)
            hr2 = ECGService.calculate_heart_rate(second_half)
            
            if hr1 and hr2 and abs(hr1 - hr2) > 10:
                abnormalities.append("Irregular rhythm detected")
        
        return abnormalities
    
    @staticmethod
    def calculate_confidence(readings: List[float]) -> float:
        """Calculate confidence score for analysis"""
        if len(readings) < 100:
            return 0.0
        
        # Simple confidence calculation based on data quality
        signal_strength = np.std(readings)
        data_length = len(readings)
        
        # Normalize confidence (0-1)
        confidence = min(1.0, (signal_strength / 100) * (data_length / 1000))
        
        return round(confidence, 2) 