#!/usr/bin/env python3
"""
Test script for Family Invite Code functionality
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8001"

def get_access_token(email, password):
    """Get access token for testing"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    return response.json()["access_token"]

def test_invite_code_flow():
    """Test the complete invite code flow"""
    
    # Get access token for family owner
    owner_token = get_access_token("patient@example.com", "securepassword123")
    
    print("🔑 Got owner access token")
    
    # Get invite code
    headers = {"Authorization": f"Bearer {owner_token}"}
    response = requests.get(f"{BASE_URL}/family/invite-code", headers=headers)
    
    if response.status_code == 200:
        invite_data = response.json()
        invite_code = invite_data["invite_code"]
        family_name = invite_data["family_name"]
        
        print(f"📋 Invite Code: {invite_code}")
        print(f"👨‍👩‍👧‍👦 Family Name: {family_name}")
        
        # Now test joining with this invite code
        print("\n🧪 Testing join with invite code...")
        
        # Get access token for new member
        member_token = get_access_token("family2@example.com", "securepassword123")
        
        join_response = requests.post(f"{BASE_URL}/family/join", 
                                   headers={"Authorization": f"Bearer {member_token}",
                                           "Content-Type": "application/json"},
                                   json={"invite_code": invite_code})
        
        if join_response.status_code == 200:
            print("✅ Successfully joined family!")
            print(f"📄 Response: {json.dumps(join_response.json(), indent=2)}")
        else:
            print(f"❌ Failed to join family: {join_response.json()}")
    
    else:
        print(f"❌ Failed to get invite code: {response.json()}")

if __name__ == "__main__":
    print("🚀 Testing Family Invite Code Flow")
    print("=" * 40)
    test_invite_code_flow() 