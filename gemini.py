import os
import sys
import requests
import json
from core.rotator import SmartRotator
from core.infra import CloudInfra
from core.repair import AutoHealer
from core.db import CloudDB

class AutonomousAgent:
    def __init__(self):
        self.rotator = SmartRotator()
        self.infra = CloudInfra()
        self.healer = AutoHealer()
        self.db = CloudDB()
        self.max_retries = 5

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_retries:
            return "❌ Error: All keys failed. This usually means a Region Block or invalid keys."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key found."
        
        # Absolute Stable Path (Fixed 404 issue)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        
        params = {'key': apiKey}
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        try:
            # Using v1 stable instead of v1beta to avoid 404 pathing errors
            res = requests.post(url, params=params, headers=headers, json=payload, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                if 'candidates' in data:
                    return data['candidates'][0]['content']['parts'][0]['text']
            
            # Diagnostic Log
            print(f"⚠️ Key #{self.rotator.gemini_index} Rejected (Status: {res.status_code})")
            
            # If 404 or 403, rotate immediately
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
            
        except Exception as e:
            return f"❌ Connection Failure: {e}"

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"Bridge Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status report."
    agent.run_autonomous_cycle(query)
