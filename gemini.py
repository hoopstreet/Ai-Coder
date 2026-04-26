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
            return "❌ Error: Free Tier Limit reached or Region Blocked."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key found."
        
        # Free Tier works best with v1beta + 1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apiKey}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        try:
            # Free tier needs clear headers and JSON structure
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            data = res.json()
            
            if res.status_code == 200:
                if 'candidates' in data and data['candidates']:
                    return data['candidates'][0]['content']['parts'][0]['text']
            
            # Handle specific Free Tier codes (429: Quota, 403: Forbidden/Region)
            print(f"⚠️ Key #{self.rotator.gemini_index} failed (Code: {res.status_code}). Rotating...")
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
            
        except Exception as e:
            return f"❌ Connection Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"Free-Tier Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Audit repo."
    agent.run_autonomous_cycle(query)
