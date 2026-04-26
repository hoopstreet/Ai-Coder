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
        self.system_prompt = "You are a Self-Healing Enterprise AI Agent."

    def call_ai(self, prompt, model="gemini-2.5-flash-preview-09-2025"):
        apiKey = self.rotator.get_gemini_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 429:
                self.rotator.rotate_on_fail()
                return self.call_ai(prompt, model)
            return res.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error: {e}"

    def run_autonomous_cycle(self, user_query=None):
        # Step 1: Health Audit
        has_issues = self.healer.check_all_systems()
        audit_status = "CRITICAL" if has_issues else "HEALTHY"
        
        # Log Audit to Cloud
        self.db.log_event("AUDIT_CHECK", f"Status: {audit_status}")

        if has_issues:
            print("🚨 Issues detected! Initiating AI-AutoFix...")
            fix = self.call_ai("The system audit failed. Provide a fix.")
            print(f"🤖 AI Suggestion: {fix}")
        
        if user_query:
            self.healer.show_spinner(f"Processing: {user_query}", 2)
            response = self.call_ai(user_query)
            self.db.log_event("AI_QUERY", f"Query: {user_query[:50]}")
            print(f"\n🤖 OUTPUT:\n{response}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    agent.run_autonomous_cycle(query)
