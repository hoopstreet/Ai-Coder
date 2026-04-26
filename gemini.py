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
            return "❌ Error: All API keys exhausted or model unavailable."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key available."
        
        # Use v1 endpoint for 1.5-flash stability
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=20)
            data = res.json()
            
            if res.status_code == 429 or res.status_code == 404:
                self.rotator.rotate_on_fail()
                return self.call_ai(prompt, model, attempt + 1)
            
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                msg = data.get('error', {}).get('message', 'Unknown Error')
                return f"❌ API Error: {msg}"
        except Exception as e:
            return f"❌ Connection Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        # Health check without blocking
        self.healer.check_all_systems()
        
        if user_query:
            self.healer.show_spinner(f"AI Processing", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Check system health."
    agent.run_autonomous_cycle(query)
