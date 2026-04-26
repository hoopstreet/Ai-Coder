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
        # OpenRouter Key from Config
        self.or_key = self.rotator.config.get("OPENROUTER_API_KEY", "")

    def call_openrouter(self, prompt):
        """Backup Agent: Triggered when Gemini fails."""
        print("🔌 Switching to Backup Agent (OpenRouter)...")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.or_key}",
            "HTTP-Referer": "https://github.com/hoopstreet/Ai-Coder",
            "Content-Type": "application/json"
        }
        # Using a reliable free model as failover
        payload = {
            "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                return data['choices'][0]['message']['content']
            return f"❌ OpenRouter Error: {res.status_code}"
        except Exception as e:
            return f"❌ Backup Agent Failure: {e}"

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_retries:
            # TRIGGER FAILOVER
            if self.or_key:
                return self.call_openrouter(f"Gemini API is down (Status 404/403). Diagnose and help with: {prompt}")
            return "❌ Error: All Gemini keys failed and no OpenRouter key found."
            
        apiKey = self.rotator.get_gemini_key()
        # Free Tier v1beta is often the only one that works for free keys
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apiKey}"
        
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            
            print(f"⚠️ Key #{self.rotator.gemini_index} Failed ({res.status_code}). Rotating...")
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
        except:
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)

    def run_autonomous_cycle(self, user_query=None):
        self.healer.check_all_systems()
        if user_query:
            self.healer.show_spinner(f"Hybrid Sync", 1)
            response = self.call_ai(user_query)
            print(f"\n🤖 AGENT RESPONSE:\n{response}")
            self.db.log_event("SUCCESS", f"Query: {user_query[:30]}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status report."
    agent.run_autonomous_cycle(query)
