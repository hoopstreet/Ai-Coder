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
        self.system_prompt = "You are a Self-Healing Enterprise AI Agent. Output only technical results."

    def call_ai(self, prompt, model="gemini-2.0-flash"):
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key available."
        
        # Public v1beta endpoint with stable model name
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=30)
            data = res.json()
            
            if res.status_code == 429:
                self.rotator.rotate_on_fail()
                return self.call_ai(prompt, model)
            
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"❌ API Error: {data.get('error', {}).get('message', 'Unknown Error')}"
        except Exception as e:
            return f"❌ Execution Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        has_issues = self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"AI Processing", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status check."
    agent.run_autonomous_cycle(query)
