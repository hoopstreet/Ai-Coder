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
        self.max_gemini_retries = 5
        # Credentials are now pulled from the internal rotator config
        # to prevent GitHub Push Protection triggers
        self.or_key = self.rotator.config.get("OPENROUTER_API_KEY")

    def call_openrouter(self, prompt):
        models = [
            "google/gemini-2.0-flash-lite-preview-02-05:free",
            "google/gemini-2.0-pro-exp-02-05:free",
            "deepseek/deepseek-chat:free"
        ]
        print("🔌 Failover Active (Gemini -> OpenRouter)...")
        for m in models:
            try:
                print(f"📡 Testing Model: {m}")
                res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.or_key}",
                        "HTTP-Referer": "https://github.com/hoopstreet/Ai-Coder",
                        "Content-Type": "application/json"
                    },
                    json={"model": m, "messages": [{"role": "user", "content": prompt}]}, 
                    timeout=25)
                if res.status_code == 200: 
                    return res.json()['choices'][0]['message']['content']
            except: continue
        return "❌ All models failed."

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_gemini_retries: return self.call_openrouter(prompt)
        apiKey = self.rotator.get_gemini_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apiKey}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if res.status_code == 200: return res.json()['candidates'][0]['content']['parts'][0]['text']
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
        except:
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)

    def run_autonomous_cycle(self, query=None):
        self.healer.check_all_systems()
        if query:
            print(f"\n🤖 AGENT RESPONSE:\n{self.call_ai(query)}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    agent.run_autonomous_cycle(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status check.")
