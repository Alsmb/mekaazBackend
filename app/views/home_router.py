from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.controllers.home_controller import HomeController

router = APIRouter(prefix="/home", tags=["Home"])

@router.get("/kpi")
def get_kpis(current_user: User = Depends(get_current_user)):
    return HomeController.get_kpis(current_user.id, None)

@router.get("/protected")
def protected_home(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}! This is a protected endpoint."} 