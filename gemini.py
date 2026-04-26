import os, sys, requests, json, time, subprocess

class SingularityV3:
    def __init__(self):
        self.repo = "/root/Ai-Coder"
        # Recovered Configs from Northflank Deployment Audit
        self.supabase_schema = "public"
        self.bot_logging = True
        self.keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas", "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA", "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY", "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg", "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"

    def log(self, msg):
        prefix = "🤖 [SINGULARITY v3.0.0]"
        with open(f"{self.repo}/master.log", "a") as f: f.write(f"[{time.ctime()}] {msg}\n")
        print(f"{prefix} {msg}")

    def sync(self):
        try:
            ts = int(time.time())
            tag = f"v3.0.0-recovery-{ts}"
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"feat: Integrated Northflank State {tag}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            subprocess.run(["git", "tag", tag], cwd=self.repo)
            subprocess.run(["git", "push", "origin", tag], cwd=self.repo)
            self.log(f"🌍 Recovered State Tagged: {tag}")
        except: pass

    def deep_analyze(self, prompt):
        # Full history context injection
        context = "CONTEXT: Northflank Deployments, Supabase Schema, GitHub Auth enabled. TASK: "
        for k in self.keys:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}", 
                    json={"contents": [{"parts": [{"text": context + prompt}]}]}, timeout=15)
                if r.status_code == 200: return r.json()['candidates'][0]['content']['parts'][0]['text']
            except: continue
        return None

if __name__ == "__main__":
    agent = SingularityV3()
    if len(sys.argv) > 1 and sys.argv[1] == "AUTO_SYNC":
        agent.sync()
    else:
        task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Perform Full System Adoption"
        res = agent.deep_analyze(task)
        if res:
            with open(f"{agent.repo}/RECOVERYLOGS.md", "a") as f:
                f.write(f"\n\n## 🛰️ DEPLOYMENT RECOVERY [{time.ctime()}]\n{res}")
            agent.sync()
