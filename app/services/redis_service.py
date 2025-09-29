import redis
import json
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings

class RedisService:
    def __init__(self):
        # Get Redis URL from environment or use default
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
    
    def store_live_vital(self, user_id: str, vital_data: Dict[str, Any]) -> bool:
        """Store live vital data for real-time access"""
        key = f"live_vital:{user_id}"
        vital_data['timestamp'] = datetime.utcnow().isoformat()
        self.redis_client.setex(key, 300, json.dumps(vital_data))  # 5 minutes TTL
        return True
    
    def get_live_vital(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get latest vital data for user"""
        key = f"live_vital:{user_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def store_vital_aggregate(self, user_id: str, period: str, aggregate_data: Dict[str, Any]) -> bool:
        """Store aggregated vital data for charts"""
        key = f"vital_aggregate:{user_id}:{period}"
        self.redis_client.setex(key, 3600, json.dumps(aggregate_data))  # 1 hour TTL
        return True
    
    def get_vital_aggregate(self, user_id: str, period: str) -> Optional[Dict[str, Any]]:
        """Get aggregated vital data for charts"""
        key = f"vital_aggregate:{user_id}:{period}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def store_device_status(self, device_id: str, status: Dict[str, Any]) -> bool:
        """Store device connection status"""
        key = f"device_status:{device_id}"
        self.redis_client.setex(key, 600, json.dumps(status))  # 10 minutes TTL
        return True
    
    def get_device_status(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get device connection status"""
        key = f"device_status:{device_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def publish_vital_update(self, user_id: str, vital_data: Dict[str, Any]) -> bool:
        """Publish vital update to WebSocket subscribers"""
        channel = f"vital_updates:{user_id}"
        self.redis_client.publish(channel, json.dumps(vital_data))
        return True

# Global Redis service instance
redis_service = RedisService() 