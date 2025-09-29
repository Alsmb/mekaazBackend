from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, LanguageEnum

class UserResponse(BaseModel):
    id: str
    email: str
    phone_number: Optional[str]
    name: Optional[str]
    role: UserRole
    language: Optional[LanguageEnum]
    is_phone_verified: bool
    is_email_verified: bool
    created_at: Optional[datetime]

class UserUpdateRequest(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    language: Optional[LanguageEnum]

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole
    phone_number: Optional[str] = None
    language: LanguageEnum = LanguageEnum.EN 