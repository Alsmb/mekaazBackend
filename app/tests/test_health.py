import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.models.user import UserRole, LanguageEnum
from app.models.device import Device
from app.models.vitals import Vital
import uuid
from datetime import datetime

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "role": UserRole.PATIENT,
        "phone_number": "+1234567890",
        "language": LanguageEnum.EN
    }

@pytest.fixture
def authenticated_client(test_user_data):
    """Create authenticated client with user and device"""
    # Create user
    signup_response = client.post("/auth/signup", json=test_user_data)
    access_token = signup_response.json()["access_token"]
    
    # Create device
    device_data = {
        "device_id": "test_device_123",
        "device_type": "heart_monitor",
        "device_name": "Test Device"
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    client.post("/devices/connect", json=device_data, headers=headers)
    
    return client, access_token

class TestVitalsEndpoints:
    def test_ingest_vital_data(self, authenticated_client):
        """Test vital data ingestion"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        vital_data = {
            "device_id": "test_device_123",
            "heart_rate": 75,
            "spo2": 98.5,
            "temperature": 36.8,
            "steps": 1000,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "respiratory_rate": 16
        }
        
        response = client.post("/vitals/ingest", json=vital_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["heart_rate"] == 75
        assert data["spo2"] == 98.5
    
    def test_get_vital_history(self, authenticated_client):
        """Test getting vital history"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # First ingest some data
        vital_data = {
            "device_id": "test_device_123",
            "heart_rate": 75,
            "spo2": 98.5
        }
        client.post("/vitals/ingest", json=vital_data, headers=headers)
        
        # Get history
        response = client.get("/vitals/history", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
    
    def test_get_live_vital(self, authenticated_client):
        """Test getting live vital data"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # First ingest some data
        vital_data = {
            "device_id": "test_device_123",
            "heart_rate": 75,
            "spo2": 98.5
        }
        client.post("/vitals/ingest", json=vital_data, headers=headers)
        
        # Get live data
        response = client.get("/vitals/live", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "heart_rate" in data
    
    def test_get_chart_data(self, authenticated_client):
        """Test getting chart data"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # First ingest some data
        vital_data = {
            "device_id": "test_device_123",
            "heart_rate": 75,
            "spo2": 98.5
        }
        client.post("/vitals/ingest", json=vital_data, headers=headers)
        
        # Get chart data
        response = client.get("/vitals/charts/hour", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "period" in data

class TestDeviceEndpoints:
    def test_connect_device(self, authenticated_client):
        """Test device connection"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        device_data = {
            "device_id": "new_device_456",
            "device_type": "ecg_device",
            "device_name": "New ECG Device"
        }
        
        response = client.post("/devices/connect", json=device_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["device_id"] == "new_device_456"
    
    def test_get_available_devices(self, authenticated_client):
        """Test getting available devices"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.get("/devices/available", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "devices" in data
    
    def test_disconnect_device(self, authenticated_client):
        """Test device disconnection"""
        client, access_token = authenticated_client
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = client.delete("/devices/test_device_123", headers=headers)
        assert response.status_code == 200 