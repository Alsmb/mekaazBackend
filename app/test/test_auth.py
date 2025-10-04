# app/tests/test_auth.py
import pytest
from app.models.user import UserRole, LanguageEnum

def test_signup_success(test_client):
    user_data = {
        "email": "auth_user@example.com",
        "password": "testpassword123",
        "name": "Test Auth User",
        "role": UserRole.PATIENT,
        "phone_number": "+1234567890",
        "language": LanguageEnum.EN
    }

    response = test_client.post("/auth/signup", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_success(test_client):
    email = "auth_user2@example.com"
    password = "testpassword123"
    signup_data = {
        "email": email,
        "password": password,
        "name": "Login Test User",
        "role": UserRole.PATIENT,
        "phone_number": "+1234567899",
        "language": LanguageEnum.EN
    }
    test_client.post("/auth/signup", json=signup_data)

    response = test_client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data




# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.core.database import Base, get_db
# from app.main import app
# from app.models.user import UserRole, LanguageEnum
# from app.core.security import get_password_hash
# import uuid

# # Test database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)

# @pytest.fixture(autouse=True)
# def setup_database():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)

# @pytest.fixture
# def test_user_data():
#     return {
#         "email": "test@example.com",
#         "password": "testpassword123",
#         "name": "Test User",
#         "role": UserRole.PATIENT,
#         "phone_number": "+1234567890",
#         "language": LanguageEnum.EN
#     }

# class TestAuthentication:
#     def test_signup_success(self, test_user_data):
#         """Test successful user signup"""
#         response = client.post("/auth/signup", json=test_user_data)
#         assert response.status_code == 200
#         data = response.json()
#         assert "access_token" in data
#         assert "refresh_token" in data
#         assert data["token_type"] == "bearer"
    
#     def test_signup_duplicate_email(self, test_user_data):
#         """Test signup with duplicate email"""
#         # First signup
#         client.post("/auth/signup", json=test_user_data)
        
#         # Second signup with same email
#         response = client.post("/auth/signup", json=test_user_data)
#         assert response.status_code == 400
#         assert "Email already registered" in response.json()["detail"]
    
#     def test_login_success(self, test_user_data):
#         """Test successful login"""
#         # Create user first
#         client.post("/auth/signup", json=test_user_data)
        
#         # Login
#         login_data = {
#             "email": test_user_data["email"],
#             "password": test_user_data["password"]
#         }
#         response = client.post("/auth/login", json=login_data)
#         assert response.status_code == 200
#         data = response.json()
#         assert "access_token" in data
#         assert "refresh_token" in data
    
#     def test_login_invalid_credentials(self, test_user_data):
#         """Test login with invalid credentials"""
#         # Create user first
#         client.post("/auth/signup", json=test_user_data)
        
#         # Login with wrong password
#         login_data = {
#             "email": test_user_data["email"],
#             "password": "wrongpassword"
#         }
#         response = client.post("/auth/login", json=login_data)
#         assert response.status_code == 401
#         assert "Invalid credentials" in response.json()["detail"]
    
#     def test_refresh_token(self, test_user_data):
#         """Test token refresh"""
#         # Create user and get tokens
#         signup_response = client.post("/auth/signup", json=test_user_data)
#         refresh_token = signup_response.json()["refresh_token"]
        
#         # Refresh token
#         response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
#         assert response.status_code == 200
#         data = response.json()
#         assert "access_token" in data
#         assert "refresh_token" in data

# class TestProtectedEndpoints:
#     def test_protected_endpoint_with_token(self, test_user_data):
#         """Test accessing protected endpoint with valid token"""
#         # Create user and get token
#         signup_response = client.post("/auth/signup", json=test_user_data)
#         access_token = signup_response.json()["access_token"]
        
#         # Access protected endpoint
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = client.get("/user/me", headers=headers)
#         assert response.status_code == 200
    
#     def test_protected_endpoint_without_token(self):
#         """Test accessing protected endpoint without token"""
#         response = client.get("/user/me")
#         assert response.status_code == 401
    
#     def test_protected_endpoint_with_invalid_token(self):
#         """Test accessing protected endpoint with invalid token"""
#         headers = {"Authorization": "Bearer invalid_token"}
#         response = client.get("/user/me", headers=headers)
#         assert response.status_code == 401 