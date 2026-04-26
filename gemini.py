import os, sys, requests, json, time, subprocess

class AutonomousSingularity:
    def __init__(self):
        self.repo = "/root/Ai-Coder"
        self.gemini_keys = [
            "AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas",
            "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA",
            "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY",
            "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg",
            "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"
        ]
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"
        self.free_models = ["google/gemini-2.0-flash-lite-preview-02-05:free", "deepseek/deepseek-r1:free", "openrouter/auto"]
        self.paid_models = ["google/gemini-2.0-flash-001", "google/gemini-pro-1.5"]

    def log(self, msg):
        with open(f'{self.repo}/master.log', 'a') as f:
            f.write(f"[{time.ctime()}] {msg}\n")
        print(f"🤖 {msg}")

    def call_or(self, prompt, models):
        for m in models:
            try:
                self.log(f"Failover Attempt: {m}")
                res = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.or_key}"},
                    json={"model": m, "messages": [{"role": "user", "content": prompt}]}, timeout=30)
                if res.status_code == 200: return res.json()['choices'][0]['message']['content']
            except: continue
        return None

    def ask(self, prompt):
        # TIER 1: Gemini Pool
        for k in self.gemini_keys:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                if r.status_code == 200: return r.json()['candidates'][0]['content']['parts'][0]['text']
            except: continue
        
        # TIER 2 & 3: OpenRouter
        self.log("⚠️ Gemini Pool Limited. Switching to OpenRouter...")
        res = self.call_or(prompt, self.free_models)
        if res: return res
        self.log("🚨 Free Tier Limited. Using Paid Escalation...")
        return self.call_or(prompt, self.paid_models)

    def sync(self):
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"Autonomic Sync {time.ctime()}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            self.log("🌍 GitHub Mirror Updated.")
        except: pass

if __name__ == "__main__":
    agent = AutonomousSingularity()
    if len(sys.argv) > 1:
        if sys.argv[1] == "AUTO_SYNC":
            agent.sync()
        else:
            task = " ".join(sys.argv[1:])
            ans = agent.ask(task)
            if ans:
                with open(f"{agent.repo}/RECOVERYLOGS.md", "a") as f:
                    f.write(f"\n\n### [v2.8.1 Failover Log - {time.ctime()}]\n{ans[:500]}...")
                agent.sync()
