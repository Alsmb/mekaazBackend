from pydantic import BaseModel
from typing import Optional
from app.models.user import UserRole, LanguageEnum

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    role: UserRole
    phone_number: Optional[str] = None
    language: LanguageEnum = LanguageEnum.EN

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer" 