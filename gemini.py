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
        self.max_retries = 10 # Increased to cover the full matrix

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_retries:
            return "❌ Error: API handshake failed. All models (Pro/Flash/Lite) rejected these keys."
            
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key found."
        
        # Comprehensive Model Matrix based on Gemini CLI docs
        configs = [
            {"v": "v1beta", "m": "gemini-2.5-flash-preview-09-2025"}, # Auto (Gemini 2.5)
            {"v": "v1beta", "m": "gemini-1.5-flash-002"},             # Flash Optimized
            {"v": "v1beta", "m": "gemini-1.5-pro-002"},               # Pro Reasoning
            {"v": "v1beta", "m": "gemini-1.5-flash-8b"},             # Flash-Lite
            {"v": "v1",     "m": "gemini-1.5-flash"},                # Stable Production
            {"v": "v1beta", "m": "gemini-1.0-pro"}                    # Legacy Fallback
        ]
        
        cfg = configs[attempt % len(configs)]
        url = f"https://generativelanguage.googleapis.com/{cfg['v']}/models/{cfg['m']}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
            
            if res.status_code == 200 and 'candidates' in data:
                return data['candidates'][0]['content']['parts'][0]['text']
            
            # If rejected (404, 403, 400), rotate key OR try next model
            if attempt % 2 == 0:
                self.rotator.rotate_on_fail()
            
            return self.call_ai(prompt, attempt + 1)
            
        except Exception as e:
            return f"❌ Connection Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"Auto-Model Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Audit repo state."
    agent.run_autonomous_cycle(query)
