import random
import string
from typing import Optional

class SMSService:
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp(phone_number: str, otp_code: str) -> bool:
        """
        Send OTP via SMS
        In production, integrate with Twilio, AWS SNS, or similar service
        """
        # Mock implementation for development
        print(f"SMS OTP sent to {phone_number}: {otp_code}")
        return True
    
    @staticmethod
    def send_emergency_alert(phone_number: str, message: str) -> bool:
        """
        Send emergency alert via SMS
        """
        # Mock implementation for development
        print(f"Emergency SMS sent to {phone_number}: {message}")
        return True 