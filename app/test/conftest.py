# app/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app

# Use SQLite test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override DB dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="session")
def test_client():
    return client

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# import pytest
# import requests
# import time

# BASE_URL = "http://localhost:8000"
# TEST_EMAIL = f"testuser{int(time.time())}@example.com"
# TEST_PASSWORD = "testpass123"
# TEST_NAME = "Test User"
# TEST_PHONE = f"+1234567{int(time.time()) % 10000:04d}"


# @pytest.fixture(scope="session")
# def test_user():
#     """Signup or login and return user credentials"""
#     data = {
#         "email": TEST_EMAIL,
#         "password": TEST_PASSWORD,
#         "name": TEST_NAME,
#         "role": "patient",
#         "phone_number": TEST_PHONE,
#         "language": "EN"
#     }
#     resp = requests.post(f"{BASE_URL}/auth/signup", json=data)

#     if resp.status_code == 200:
#         token = resp.json()["access_token"]
#     else:
#         # Try login if already exists
#         resp = requests.post(f"{BASE_URL}/auth/login", json={
#             "email": TEST_EMAIL,
#             "password": TEST_PASSWORD
#         })
#         token = resp.json()["access_token"]

#     return {
#         "email": TEST_EMAIL,
#         "password": TEST_PASSWORD,
#         "access_token": token
#     }


# @pytest.fixture(scope="session")
# def access_token(test_user):
#     """Provide only the access_token for convenience"""
#     return test_user["access_token"]