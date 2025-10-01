import pytest
import requests
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"testuser{int(time.time())}@example.com"
TEST_PASSWORD = "testpass123"
TEST_NAME = "Test User"
TEST_PHONE = f"+1234567{int(time.time()) % 10000:04d}"


@pytest.fixture(scope="session")
def test_user():
    """Signup or login and return user credentials"""
    data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "name": TEST_NAME,
        "role": "patient",
        "phone_number": TEST_PHONE,
        "language": "EN"
    }
    resp = requests.post(f"{BASE_URL}/auth/signup", json=data)

    if resp.status_code == 200:
        token = resp.json()["access_token"]
    else:
        # Try login if already exists
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        token = resp.json()["access_token"]

    return {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "access_token": token
    }


@pytest.fixture(scope="session")
def access_token(test_user):
    """Provide only the access_token for convenience"""
    return test_user["access_token"]