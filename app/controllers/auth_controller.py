from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import uuid
from datetime import datetime

class AuthController:
    @staticmethod
    def signup(db: Session, data):
        # Check if user exists by email
        existing_user = db.query(User).filter_by(email=data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if phone number is provided and not already used
        if data.phone_number:
            existing_phone = db.query(User).filter_by(phone_number=data.phone_number).first()
            if existing_phone:
                raise HTTPException(status_code=400, detail="Phone number already registered")
        
        # Create user
        hashed_pw = get_password_hash(data.password)
        user = User(
            
            email=data.email,
            phone_number=data.phone_number,
            hashed_password=hashed_pw,
            name=data.name,
            role=data.role,
            language=data.language,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)


        
        
        # Create tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    def login(db: Session, data):
        # Try to find user by email or phone
        user = None
        if data.email:
            user = db.query(User).filter_by(email=data.email).first()
        elif hasattr(data, 'phone_number') and data.phone_number:
            user = db.query(User).filter_by(phone_number=data.phone_number).first()
        
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        } 