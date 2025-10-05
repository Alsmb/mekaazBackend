# app/tests/test_invite_code.py
import pytest
from app.models.user import UserRole, LanguageEnum

@pytest.fixture
def family_owner_token(test_client):
    data = {
        "email": "owner@example.com",
        "password": "securepassword123",
        "name": "Owner",
        "role": UserRole.PATIENT.value,
        "phone_number": "+1111111111",
        "language": LanguageEnum.EN.value
    }
    response = test_client.post("/auth/signup", json=data)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def family_member_token(test_client):
    data = {
        "email": "member@example.com",
        "password": "securepassword123",
        "name": "Member",
        "role": UserRole.PATIENT.value,
        "phone_number": "+2222222222",
        "language": LanguageEnum.EN.value
    }
    response = test_client.post("/auth/signup", json=data)
    assert response.status_code == 200
    return response.json()["access_token"]

def test_invite_code_flow(test_client, family_owner_token, family_member_token):
    """Simulate creating and joining a family"""
    headers = {"Authorization": f"Bearer {family_owner_token}"}

    # Step 1: Get invite code
    resp = test_client.get("/family/invite-code", headers=headers)
    assert resp.status_code == 200
    invite_code = resp.json()["invite_code"]

    # Step 2: Join with invite code
    headers = {"Authorization": f"Bearer {family_member_token}"}
    join_resp = test_client.post("/family/join", json={"invite_code": invite_code}, headers=headers)
    assert join_resp.status_code == 200




## #!/usr/bin/env python3
# """
# Test script for Family Invite Code functionality
# """

# import requests
# import json

# # Base URL
# BASE_URL = "http://localhost:8001"

# def get_access_token(email, password):
#     """Get access token for testing"""
#     response = requests.post(f"{BASE_URL}/auth/login", json={
#         "email": email,
#         "password": password
#     })
#     return response.json()["access_token"]

# def test_invite_code_flow():
#     """Test the complete invite code flow"""
    
#     # Get access token for family owner
#     owner_token = get_access_token("patient@example.com", "securepassword123")
    
#     print("🔑 Got owner access token")
    
#     # Get invite code
#     headers = {"Authorization": f"Bearer {owner_token}"}
#     response = requests.get(f"{BASE_URL}/family/invite-code", headers=headers)
    
#     if response.status_code == 200:
#         invite_data = response.json()
#         invite_code = invite_data["invite_code"]
#         family_name = invite_data["family_name"]
        
#         print(f"📋 Invite Code: {invite_code}")
#         print(f"👨‍👩‍👧‍👦 Family Name: {family_name}")
        
#         # Now test joining with this invite code
#         print("\n🧪 Testing join with invite code...")
        
#         # Get access token for new member
#         member_token = get_access_token("family2@example.com", "securepassword123")
        
#         join_response = requests.post(f"{BASE_URL}/family/join", 
#                                    headers={"Authorization": f"Bearer {member_token}",
#                                            "Content-Type": "application/json"},
#                                    json={"invite_code": invite_code})
        
#         if join_response.status_code == 200:
#             print("✅ Successfully joined family!")
#             print(f"📄 Response: {json.dumps(join_response.json(), indent=2)}")
#         else:
#             print(f"❌ Failed to join family: {join_response.json()}")
    
#     else:
#         print(f"❌ Failed to get invite code: {response.json()}")

# if __name__ == "__main__":
#     print("🚀 Testing Family Invite Code Flow")
#     print("=" * 40)
#     test_invite_code_flow()