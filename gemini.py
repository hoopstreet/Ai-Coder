import os
import sys
import requests
import json
import time

# Attempting local imports with safety
try:
    from core.rotator import SmartRotator
    from core.infra import CloudInfra
    from core.repair import AutoHealer
    from core.db import CloudDB
except ImportError:
    print("⚠️ Core modules missing. Ensure /root/Ai-Coder/core exists.")
    sys.exit(1)

class AutonomousAgent:
    def __init__(self):
        self.rotator = SmartRotator()
        self.db = CloudDB()
        self.healer = AutoHealer()
        self.infra = CloudInfra()
        self.max_gemini_retries = 5
        self.creds = {}
        self._orchestrate_credentials()

    def _orchestrate_credentials(self):
        """Finds and syncs credentials with failover logic."""
        print("🔍 [ORCHESTRATOR] Auditing credential sources...")
        required = ["GITHUB_TOKENS", "OPENROUTER_API_KEY", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE"]
        
        # FIX: Added internal fallback if get_config is missing from CloudDB
        try:
            cloud_creds = self.db.get_config("system_creds") or {}
        except AttributeError:
            print("⚠️ CloudDB.get_config not found. Falling back to local/env.")
            cloud_creds = {}

        local_creds = self.rotator.config
        updated = False
        
        for key in required:
            # Multi-stage lookup
            val = os.environ.get(key) or cloud_creds.get(key) or local_creds.get(key)
            if val:
                self.creds[key] = val
                if key not in local_creds or local_creds[key] != val:
                    self.rotator.config[key] = val
                    updated = True
        
        if updated:
            try:
                self.rotator.save_config()
                print("🔄 [SYNC] Local config secured.")
            except: pass

    def get_token(self, key):
        return self.creds.get(key) or self.rotator.config.get(key)

    def call_ai(self, prompt, attempt=0):
        if attempt >= self.max_gemini_retries:
            return self.call_openrouter(prompt)
        
        apiKey = self.rotator.get_gemini_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apiKey}"
        try:
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)
        except:
            self.rotator.rotate_on_fail()
            return self.call_ai(prompt, attempt + 1)

    def call_openrouter(self, prompt):
        token = self.get_token("OPENROUTER_API_KEY")
        if not token: return "❌ No OpenRouter Key."
        models = ["google/gemini-2.0-flash-lite-preview-02-05:free", "deepseek/deepseek-chat:free"]
        for m in models:
            try:
                res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                    json={"model": m, "messages": [{"role": "user", "content": prompt}]}, timeout=20)
                if res.status_code == 200: return res.json()['choices'][0]['message']['content']
            except: continue
        return "❌ All AI routes exhausted."

    def run(self, query):
        self.healer.check_all_systems()
        print(f"\n🤖 [v2.5.6] AGENT ONLINE\n{self.call_ai(query)}")

if __name__ == "__main__":
    agent = AutonomousAgent()
    agent.run(" ".join(sys.argv[1:]) if len(sys.argv) > 1 else "System check.")
