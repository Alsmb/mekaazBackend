#!/usr/bin/env python3
"""
Mekaaz API Test Script
Tests all major endpoints and functionality
"""

# import requests
# import json
# import time

# # API Configuration
# BASE_URL = "http://localhost:8000"
# TEST_EMAIL = f"testuser{int(time.time())}@example.com"
# TEST_PASSWORD = "testpass123"
# TEST_NAME = "Test User"
# TEST_PHONE = f"+1234567{int(time.time()) % 10000:04d}"

# def print_test_result(test_name, success, response=None, error=None):
#     """Print test result with formatting"""
#     if success:
#         print(f"✅ {test_name}: PASSED")
#         if response:
#             print(f"   Response: {response}")
#     else:
#         print(f"❌ {test_name}: FAILED")
#         if error:
#             print(f"   Error: {error}")
#     print()

# def test_health_check():
#     """Test health check endpoint"""
#     try:
#         response = requests.get(f"{BASE_URL}/health")
#         success = response.status_code == 200
#         print_test_result("Health Check", success, response.json() if success else None)
#         return success
#     except Exception as e:
#         print_test_result("Health Check", False, error=str(e))
#         return False

# def test_api_docs():
#     """Test API documentation endpoint"""
#     try:
#         response = requests.get(f"{BASE_URL}/docs")
#         success = response.status_code == 200
#         print_test_result("API Documentation", success)
#         return success
#     except Exception as e:
#         print_test_result("API Documentation", False, error=str(e))
#         return False

# def test_signup():
#     """Test user signup"""
#     try:
#         data = {
#             "email": TEST_EMAIL,
#             "password": TEST_PASSWORD,
#             "name": TEST_NAME,
#             "role": "patient",
#             "phone_number": TEST_PHONE,
#             "language": "EN"
#         }
#         response = requests.post(f"{BASE_URL}/auth/signup", json=data)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("User Signup", success, f"User created with ID: {result.get('access_token', 'N/A')[:20]}...")
#             return result.get('access_token')
#         else:
#             print_test_result("User Signup", success, error=response.text)
#             return None
#     except Exception as e:
#         print_test_result("User Signup", False, error=str(e))
#         return None

# def test_login():
#     """Test user login"""
#     try:
#         data = {
#             "email": TEST_EMAIL,
#             "password": TEST_PASSWORD
#         }
#         response = requests.post(f"{BASE_URL}/auth/login", json=data)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("User Login", success, f"Login successful, token: {result.get('access_token', 'N/A')[:20]}...")
#             return result.get('access_token')
#         else:
#             print_test_result("User Login", success, error=response.text)
#             return None
#     except Exception as e:
#         print_test_result("User Login", False, error=str(e))
#         return None

# def test_user_profile(access_token):
#     """Test user profile endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/user/me", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("User Profile", success, f"User: {result.get('name')} ({result.get('email')})")
#         else:
#             print_test_result("User Profile", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("User Profile", False, error=str(e))
#         return False

# def test_home_kpi(access_token):
#     """Test home KPI endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/home/kpi", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("Home KPI", success, f"KPIs: {result}")
#         else:
#             print_test_result("Home KPI", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("Home KPI", False, error=str(e))
#         return False

# def test_vitals_live(access_token):
#     """Test vitals live endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/vitals/live", headers=headers)
#         result = response.json()
        
#         # This endpoint returns 200 with "No live vital data available" when no data exists
#         # This is expected behavior for a new user
#         if response.status_code == 200:
#             if isinstance(result, dict) and "detail" in result and "No live vital data available" in result["detail"]:
#                 print_test_result("Vitals Live", True, "No data available (expected for new user)")
#                 return True
#             else:
#                 print_test_result("Vitals Live", True, f"Vitals: {result}")
#                 return True
#         else:
#             print_test_result("Vitals Live", False, error=response.text)
#             return False
#     except Exception as e:
#         print_test_result("Vitals Live", False, error=str(e))
#         return False

# def test_devices_available(access_token):
#     """Test devices available endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/devices/available", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("Devices Available", success, f"Devices: {result}")
#         else:
#             print_test_result("Devices Available", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("Devices Available", False, error=str(e))
#         return False

# def test_family_members(access_token):
#     """Test family members endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/family/members", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("Family Members", success, f"Family: {result}")
#         else:
#             print_test_result("Family Members", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("Family Members", False, error=str(e))
#         return False

# def test_analytics_health_insights(access_token):
#     """Test analytics health insights endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/analytics/health-insights", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("Analytics Health Insights", success, f"Insights: {result}")
#         else:
#             print_test_result("Analytics Health Insights", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("Analytics Health Insights", False, error=str(e))
#         return False

# def test_notifications(access_token):
#     """Test notifications endpoint"""
#     try:
#         headers = {"Authorization": f"Bearer {access_token}"}
#         response = requests.get(f"{BASE_URL}/notifications", headers=headers)
#         success = response.status_code == 200
#         if success:
#             result = response.json()
#             print_test_result("Notifications", success, f"Notifications: {result}")
#         else:
#             print_test_result("Notifications", success, error=response.text)
#         return success
#     except Exception as e:
#         print_test_result("Notifications", False, error=str(e))
#         return False

# def main():
#     """Run all tests"""
#     print("🚀 Mekaaz API Test Suite")
#     print("=" * 50)
    
#     # Test basic endpoints
#     test_health_check()
#     test_api_docs()
    
#     # Test authentication
#     print("🔐 Testing Authentication...")
#     access_token = test_signup()
#     if not access_token:
#         access_token = test_login()
    
#     if access_token:
#         print("✅ Authentication successful!")
#         print()
        
#         # Test protected endpoints
#         print("🔒 Testing Protected Endpoints...")
#         test_user_profile(access_token)
#         test_home_kpi(access_token)
#         test_vitals_live(access_token)
#         # Note: Some endpoints may have UUID compatibility issues with SQLite
#         # These will be fixed when using PostgreSQL in production
#         print("⚠️  Some endpoints may show errors due to SQLite UUID compatibility")
#         print("   This is expected in development mode with SQLite")
#         print()
        
#         print("🎉 Test suite completed!")
#     else:
#         print("❌ Authentication failed - cannot test protected endpoints")

# if __name__ == "__main__":
#     main()




import requests

BASE_URL = "http://localhost:8000"


def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok" or response.json() != {}


def test_api_docs():
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200


def test_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/user/me", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "email" in result
    assert "name" in result


def test_home_kpi(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/home/kpi", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)


def test_vitals_live(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/vitals/live", headers=headers)
    assert response.status_code == 200
    result = response.json()
    # Expected: may return "No live vital data available"
    assert isinstance(result, dict)


def test_devices_available(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/devices/available", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list) or isinstance(result, dict)


def test_family_members(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/family/members", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)


def test_analytics_health_insights(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/analytics/health-insights", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)


def test_notifications(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/notifications", headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list) or isinstance(result, dict)