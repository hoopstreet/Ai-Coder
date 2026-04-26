import os
import sys
import requests
import json
import time
from core.rotator import SmartRotator

class AutonomousAgent:
    def __init__(self):
        self.rotator = SmartRotator()
        self.history = []
        self.system_prompt = "You are an Enterprise AI-Coder Agent. Output only raw code or shell commands."

    def call_ai(self, prompt, model="gemini-2.5-flash-preview-09-2025"):
        apiKey = self.rotator.get_gemini_key()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={apiKey}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": self.system_prompt}]}
        }

        for attempt in range(5):
            try:
                response = requests.post(url, json=payload, timeout=30)
                if response.status_code == 429:
                    self.rotator.rotate_on_fail()
                    return self.call_ai(prompt, model)
                
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)
        return "❌ Error: AI exhausted."

    def auto_fix_code(self, error_log, broken_code):
        print("🔧 Auto-Fixer Triggered...")
        fix_prompt = f"Fix this code based on error: {error_log}\n\nCode:\n{broken_code}"
        return self.call_ai(fix_prompt)

if __name__ == "__main__":
    agent = AutonomousAgent()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(agent.call_ai(query))
    else:
        print("🤖 AI-Coder v1.9.0 Ready. Usage: python3 gemini.py 'your prompt'")
