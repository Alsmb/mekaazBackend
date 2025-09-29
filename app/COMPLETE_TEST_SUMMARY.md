# 🧪 **COMPLETE API TEST SUITE**

## 📋 **Test Files Overview**

### **New Test Files Created:**

#### 1. **`notifications_test.json`** - Notification System
- **Endpoints**: 6 endpoints
- **Features**: Real-time notifications, settings, unread count
- **Key Tests**:
  - Get user notifications with badges
  - Mark notifications as read
  - Notification settings management
  - Unread count tracking

#### 2. **`analytics_test.json`** - Advanced Analytics
- **Endpoints**: 6 endpoints
- **Features**: Health insights, anomaly detection, predictive health
- **Key Tests**:
  - Health insights and recommendations
  - Anomaly detection
  - Custom alerts creation
  - Health pattern analysis
  - Predictive health insights

#### 3. **`goals_test.json`** - Goal Management
- **Endpoints**: 7 endpoints
- **Features**: Goal achievements, streaks, recommendations
- **Key Tests**:
  - Goal achievements and streaks
  - Health recommendations
  - Progress tracking
  - Custom goal creation

### **Updated Test Files:**

#### 4. **`health_test.json`** - Health Monitoring (Updated)
- **Endpoints**: 9 endpoints (4 new added)
- **New Features**:
  - Health score calculation (0-100)
  - Health trends analysis
  - Health alerts
  - Goal tracking

#### 5. **`device_test.json`** - Device Management (Updated)
- **Endpoints**: 12 endpoints (6 new added)
- **New Features**:
  - Bluetooth device discovery
  - Signal strength monitoring
  - Battery level tracking
  - Device firmware management
  - Device calibration

#### 6. **`family_test.json`** - Family Management (Updated)
- **Endpoints**: 15 endpoints (4 new added)
- **New Features**:
  - Pending invites management
  - Family health dashboard
  - Health comparison across members
  - Health report generation

---

## 🚀 **How to Use These Test Files**

### **Step 1: Get Access Token**
```bash
# First, sign up and login to get your access token
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "role": "patient",
    "phone_number": "+1234567890",
    "language": "EN"
  }'

curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### **Step 2: Replace Token in Test Files**
Replace `YOUR_ACCESS_TOKEN_HERE` in all test files with your actual access token.

### **Step 3: Test Each Feature**

#### **Test Notifications:**
```bash
# Get notifications
curl -X GET http://localhost:8001/notifications \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get unread count
curl -X GET http://localhost:8001/notifications/unread-count \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Test Analytics:**
```bash
# Get health insights
curl -X GET http://localhost:8001/analytics/health-insights \
  -H "Authorization: Bearer YOUR_TOKEN"

# Detect anomalies
curl -X GET http://localhost:8001/analytics/anomaly-detection \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Test Goals:**
```bash
# Get goal achievements
curl -X GET http://localhost:8001/goals/achievements \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get health recommendations
curl -X GET http://localhost:8001/goals/recommendations \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Test Enhanced Health Features:**
```bash
# Get health score
curl -X GET http://localhost:8001/vitals/health-score \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get health trends
curl -X GET "http://localhost:8001/vitals/trends/heart_rate?period=week" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Test Enhanced Device Features:**
```bash
# Discover Bluetooth devices
curl -X GET http://localhost:8001/devices/discover \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get device signal strength
curl -X GET http://localhost:8001/devices/Mekaaz-1001/signal-strength \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### **Test Enhanced Family Features:**
```bash
# Get family health dashboard
curl -X GET http://localhost:8001/family/health-dashboard \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get family health comparison
curl -X GET http://localhost:8001/family/health-comparison \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 **Test Coverage Summary**

### **Total Endpoints Tested: 55+**
- **Notifications**: 6 endpoints
- **Analytics**: 6 endpoints
- **Goals**: 7 endpoints
- **Health (Enhanced)**: 9 endpoints
- **Devices (Enhanced)**: 12 endpoints
- **Family (Enhanced)**: 15 endpoints

### **Frontend Feature Coverage: 100%**
- ✅ **Health Score** (75/100 display)
- ✅ **Bluetooth Discovery** (Mekaaz-1001, 1002, 1003)
- ✅ **Signal Strength** (88% display)
- ✅ **Battery Level** (85% display)
- ✅ **Goal Achievements** (10,000 steps achieved)
- ✅ **Health Trends** (Line graphs)
- ✅ **Family Health Dashboard** (Member health status)
- ✅ **Real-time Notifications** (Badge counts)
- ✅ **Health Alerts** (Warning/critical alerts)
- ✅ **Device Firmware** (Update management)

---

## 🎯 **Testing Scenarios**

### **Scenario 1: Complete User Journey**
1. **Sign up** → Get access token
2. **Connect device** → Pair Mekaaz-1001
3. **Ingest vitals** → Send health data
4. **Check health score** → Verify 75/100 display
5. **View notifications** → Check badge count
6. **Create family** → Test invite system
7. **View family dashboard** → Check member health

### **Scenario 2: Device Management**
1. **Discover devices** → Find Mekaaz devices
2. **Check signal strength** → Verify 88% display
3. **Check battery level** → Verify 85% display
4. **Update firmware** → Test device updates
5. **Calibrate sensors** → Test calibration

### **Scenario 3: Health Analytics**
1. **Get health insights** → View recommendations
2. **Detect anomalies** → Check for alerts
3. **View health trends** → Analyze patterns
4. **Set custom alerts** → Create notifications
5. **Get predictive health** → View forecasts

### **Scenario 4: Goal Management**
1. **View achievements** → Check goal progress
2. **Get recommendations** → View health tips
3. **Record achievements** → Log goal completion
4. **Create custom goals** → Set personal targets
5. **Track streaks** → Monitor consistency

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"No live vital data available"**
   - **Solution**: First ingest vital data using `/vitals/ingest`

2. **"Device not found"**
   - **Solution**: First connect a device using `/devices/connect`

3. **"No family found"**
   - **Solution**: First create a family using `/family/create`

4. **"Health data not shared"**
   - **Solution**: Update sharing settings using `/family/sharing-settings`

### **Testing Order:**
1. **Authentication** (signup/login)
2. **Device Connection** (connect device)
3. **Health Data** (ingest vitals)
4. **Family Setup** (create/join family)
5. **Advanced Features** (analytics, goals, notifications)

---

## 📈 **Expected Results**

### **Health Score Response:**
```json
{
  "score": 85,
  "status": "Good",
  "message": "Based on 10 recent readings"
}
```

### **Device Discovery Response:**
```json
[
  {
    "device_id": "Mekaaz-1001",
    "device_name": "Mekaaz-1001",
    "device_type": "heart_monitor",
    "signal_strength": 88,
    "battery_level": 85,
    "is_available": true
  }
]
```

### **Family Health Dashboard:**
```json
{
  "family_name": "Smith Family",
  "total_members": 2,
  "healthy_members": 2,
  "members_health": [...]
}
```

---

## ✅ **Success Criteria**

Your API is **100% compatible** when you can:
- ✅ Display health score (75/100)
- ✅ Show Bluetooth device discovery
- ✅ Display signal strength (88%)
- ✅ Show battery level (85%)
- ✅ Track goal achievements
- ✅ Display health trends
- ✅ Show family health dashboard
- ✅ Display real-time notifications
- ✅ Show health alerts
- ✅ Manage device firmware

**🎉 All test files are ready for comprehensive API testing!** 


 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNTBkNTYyNS1lNWUzLTQxZjItYjdiYy00NTAyZmFkMDY1OGIiLCJleHAiOjE3NTQ5MDgwNDN9.TzliRzzrmk-pbQLlv9cth1iCslmZCvCyqydQZlmmiLI",
     
     
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNTBkNTYyNS1lNWUzLTQxZjItYjdiYy00NTAyZmFkMDY1OGIiLCJleHAiOjE3NTQ5MDg1ODd9.iHXORtpiCYoKYLJnDkSvLhDxLnulD1YiDKr6ybOZwfg",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNTBkNTYyNS1lNWUzLTQxZjItYjdiYy00NTAyZmFkMDY1OGIiLCJleHAiOjE3NTUwODEzODd9.Rr1IoEOUYl3uShJVZ_yhvz32QBj0Z-fQviK5m7TiStY",
    "token_type": "bearer"
    
    
    
    
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNTBkNTYyNS1lNWUzLTQxZjItYjdiYy00NTAyZmFkMDY1OGIiLCJleHAiOjE3NTUwODA4NDN9.3jmOu6tWVHeHTuafP3WlKeXwV98oqclSoXZSjxl6ylo",
    "token_type": "bearer"