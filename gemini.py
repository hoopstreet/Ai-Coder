import os
import sys
import requests
import json
import time
from core.rotator import SmartRotator
from core.infra import CloudInfra

class AutonomousAgent:
    def __init__(self):
        self.rotator = SmartRotator()
        self.infra = CloudInfra()
        self.system_prompt = "You are an Enterprise AI-Coder. Output only raw code or shell commands."

    def call_ai(self, prompt, model="gemini-2.5-flash-preview-09-2025"):
        apiKey = self.rotator.get_gemini_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        for attempt in range(5):
            try:
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 429:
                    self.rotator.rotate_on_fail()
                    return self.call_ai(prompt, model)
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            except:
                time.sleep(2**attempt)
        return "❌ Exhausted."

    def deploy_flow(self):
        print("🚀 Initializing Cloud Deployment...")
        self.infra.list_projects()
        self.infra.trigger_docker_build()

if __name__ == "__main__":
    agent = AutonomousAgent()
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        agent.deploy_flow()
    elif len(sys.argv) > 1:
        print(agent.call_ai(" ".join(sys.argv[1:])))
    else:
        print("🤖 AI-Coder v1.9.5 | Use 'deploy' or ask a prompt.")
