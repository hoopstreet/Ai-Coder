import os, sys, requests, json, time, subprocess

class AutonomousSingularity:
    def __init__(self):
        self.keys = [
            "AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas",
            "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA",
            "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY",
            "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg",
            "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"
        ]
        self.repo = "/root/Ai-Coder"

    def log(self, msg):
        with open(f'{self.repo}/master.log', 'a') as f:
            f.write(f"[{time.ctime()}] 🧬 {msg}\n")
        print(f"🤖 {msg}")

    def sync(self):
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"Autonomic Singularity Sync: {time.ctime()}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            self.log("✅ GitHub Cloud Mirror Synced.")
        except: pass

    def deep_analyze_and_merge(self):
        self.log("🔍 Running Deep Recursive File Audit...")
        files = subprocess.getoutput("find . -maxdepth 2 -not -path '*/.*'")
        history = ""
        if os.path.exists("RECOVERYLOGS.md"):
            with open("RECOVERYLOGS.md", "r") as f: history = f.read()
        
        prompt = f"MERGE TASK: Combine all versions v1.0.0-v2.7.0. FILES: {files}. LOGS: {history[-1000:]}. Output a unified recovery entry."
        
        for key in self.keys:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                report = res.json()['candidates'][0]['content']['parts'][0]['text']
                with open("RECOVERYLOGS.md", "a") as f:
                    f.write(f"\n\n## 🌌 SINGULARITY MERGE [{time.ctime()}]\n{report}")
                self.sync()
                return
            except: continue

if __name__ == "__main__":
    agent = AutonomousSingularity()
    if len(sys.argv) > 1 and sys.argv[1] == "AUTO_SYNC":
        agent.sync()
    else:
        agent.deep_analyze_and_merge()
