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

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_retries:
            return "❌ Error: API handshake failed. Verify API Key permissions."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key found."
        
        # Matrix of possible successful configurations
        configs = [
            {"v": "v1beta", "m": "gemini-1.5-flash-latest"},
            {"v": "v1", "m": "gemini-1.5-flash"},
            {"v": "v1beta", "m": "gemini-pro"}
        ]
        
        # Use the config based on the current attempt index to try different combos
        cfg = configs[attempt % len(configs)]
        url = f"https://generativelanguage.googleapis.com/{cfg['v']}/models/{cfg['m']}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            
            if res.status_code == 200 and 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
            
            # If rejected, rotate key and try next matrix config
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
            
        except Exception as e:
            return f"❌ Connection Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"Matrix Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Audit system."
    agent.run_autonomous_cycle(query)
