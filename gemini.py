import os
import sys
import requests
import json
import time
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

    def call_ai(self, prompt, model="gemini-1.5-flash", attempt=0):
        if attempt >= self.max_retries:
            return "❌ Error: API Authentication Failed on all rotated keys."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key found in config.enc."
        
        # Try v1beta as it is more permissive for newer keys
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=20)
            
            # Handle Quota or Key issues
            if res.status_code in [429, 403, 400]:
                self.rotator.rotate_on_fail()
                return self.call_ai(prompt, model, attempt + 1)
            
            data = res.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"❌ API Response Issue: {data.get('error', {}).get('message', 'Unknown')}"
        except Exception as e:
            # If v1beta fails connection, try v1 as fallback
            try:
                url_v1 = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={apiKey}"
                res = requests.post(url_v1, json=payload, timeout=15)
                data = res.json()
                if 'candidates' in data: return data['candidates'][0]['content']['parts'][0]['text']
            except: pass
            return f"❌ Connection Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"AI Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Health check."
    agent.run_autonomous_cycle(query)
