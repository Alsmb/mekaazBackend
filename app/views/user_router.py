from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user.to_dict()

@router.patch("/profile", response_model=UserResponse)
def update_user_profile(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    try:
        if data.name is not None:
            current_user.name = data.name
        if data.phone_number is not None:
            # Check if phone number is already taken by another user
            existing_user = db.query(User).filter(
                User.phone_number == data.phone_number,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Phone number already registered")
            current_user.phone_number = data.phone_number
        if data.language is not None:
            current_user.language = data.language
        
        db.commit()
        db.refresh(current_user)
        return current_user.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update profile") 