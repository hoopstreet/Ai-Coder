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
        self.system_prompt = "You are a Self-Healing Enterprise AI Agent. Output only relevant technical info."

    def call_ai(self, prompt, model="gemini-2.5-flash-preview-09-2025"):
        apiKey = self.rotator.get_gemini_key()
        if not apiKey: return "❌ No API Key available."
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=30)
            data = res.json()
            
            if res.status_code == 429:
                self.rotator.rotate_on_fail()
                return self.call_ai(prompt, model)
            
            # Robust parsing for candidates and safety blocks
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
            elif 'promptFeedback' in data:
                return f"⚠️ Safety Block: {data['promptFeedback'].get('blockReason')}"
            else:
                return f"❌ API Error: {json.dumps(data)}"
        except Exception as e:
            return f"❌ Execution Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        has_issues = self.healer.check_all_systems()
        audit_status = "CRITICAL" if has_issues else "HEALTHY"
        self.db.log_event("AUDIT_CHECK", f"Status: {audit_status}")

        if user_query:
            self.healer.show_spinner(f"AI Processing", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Verify system integrity."
    agent.run_autonomous_cycle(query)
