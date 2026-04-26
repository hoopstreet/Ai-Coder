import os, sys, requests, json, time, subprocess, re

class AutonomousAgent:
    def __init__(self):
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"
        self.gemini_keys = [
            "AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas",
            "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA",
            "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY",
            "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg",
            "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"
        ]
        self.repo_path = "/root/Ai-Coder"

    def log(self, msg):
        with open(f'{self.repo_path}/master.log', 'a') as f:
            f.write(f"[{time.ctime()}] {msg}\n")
        print(f"🤖 {msg}")

    def sync_github(self):
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Autonomic Sync: {time.ctime()}"], check=True)
            subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
            self.log("🌍 GitHub Sync Successful.")
        except: pass

    def run(self, task):
        self.log(f"Mission: {task}")
        # Core Engine Logic
        for key in self.gemini_keys:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": task}]}]}, timeout=15)
                text = res.json()['candidates'][0]['content']['parts'][0]['text']
                self.log("✅ Engine Response Received.")
                return text
            except: continue
        return "Failover needed."

if __name__ == "__main__":
    agent = AutonomousAgent()
    if len(sys.argv) > 1:
        res = agent.run(" ".join(sys.argv[1:]))
        # Log to documentary
        with open("/root/Ai-Coder/RECOVERYLOGS.md", "a") as f:
            f.write(f"\n\n### [v2.6.1 - {time.ctime()}]\n{res[:300]}...")
        agent.sync_github()
