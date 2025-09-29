import random
import string
from typing import Optional

class EmailService:
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def send_otp(email: str, otp_code: str) -> bool:
        """
        Send OTP via email
        In production, integrate with SendGrid, AWS SES, or similar service
        """
        # Mock implementation for development
        print(f"Email OTP sent to {email}: {otp_code}")
        return True
    
    @staticmethod
    def send_password_reset(email: str, reset_link: str) -> bool:
        """
        Send password reset email
        """
        # Mock implementation for development
        print(f"Password reset email sent to {email}: {reset_link}")
        return True 