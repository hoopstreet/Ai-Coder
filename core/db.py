import requests
import json
from core.rotator import SmartRotator

class CloudDB:
    def __init__(self):
        self.rotator = SmartRotator()
        self.config = self.rotator.config.get("SUPABASE", {})
        self.url = self.config.get("URL")
        self.key = self.config.get("SERVICE_ROLE")
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

    def log_event(self, event_type, details):
        """Logs audit or AI events to Supabase 'logs' table."""
        if not self.url: return
        endpoint = f"{self.url}/rest/v1/logs"
        payload = {
            "event_type": event_type,
            "details": details,
            "version": "2.1.0"
        }
        try:
            requests.post(endpoint, headers=self.headers, json=payload, timeout=5)
        except:
            pass # Silent fail to prevent blocking CLI flow

if __name__ == "__main__":
    db = CloudDB()
    print(f"📡 Cloud Sync Target: {db.url}")
