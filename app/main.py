from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import user, vitals, family, sos, otp, device, emergency_contact, ecg, notification

# Create all tables
Base.metadata.create_all(bind=engine)

# Import routers
from app.views import auth_router, home_router, health_router, family_router, otp_router, device_router, user_router, websocket_router, sos_router, ecg_router, notification_router, analytics_router

app = FastAPI(title="Mekaaz Backend")

# Register routers
app.include_router(auth_router.router)
app.include_router(otp_router.router)
app.include_router(user_router.router)
app.include_router(home_router.router)
app.include_router(health_router.router)
app.include_router(family_router.router)
app.include_router(device_router.router)
app.include_router(websocket_router.router)
app.include_router(sos_router.router)
app.include_router(ecg_router.router)
app.include_router(notification_router.router)
app.include_router(analytics_router.router)

@app.get("/")
def root():
    return {"message": "Mekaaz API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"} 