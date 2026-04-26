import os, sys, requests, json, time, subprocess

class SwarmGeneral:
    def __init__(self):
        self.repo = "/root/Ai-Coder"
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"
        self.gemini_keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas", "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA", "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY", "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg", "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]
        self.teams = {
            "Hive_Legacy": {"head": "google/gemini-pro-1.5", "focus": "v1.0.0-v2.7.0 upgrades"},
            "Hive_Recovery": {"head": "anthropic/claude-3.5-sonnet", "focus": "Disaster Recovery & Deployment Merges"}
        }

    def log(self, team, msg):
        log_msg = f"[{time.ctime()}] [{team}] 🛡️ {msg}"
        with open(f"{self.repo}/swarm_status.log", "a") as f: f.write(log_msg + "\n")
        print(log_msg)

    def call_head(self, team, task):
        model = self.teams[team]["head"]
        headers = {"Authorization": f"Bearer {self.or_key}", "Content-Type": "application/json"}
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                json={"model": model, "messages": [{"role": "system", "content": f"Head of {team}. Role: {self.teams[team]['focus']}"}, {"role": "user", "content": task}]}, timeout=45)
            return res.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

    def sync_all(self):
        try:
            ts = int(time.time())
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"Swarm Update v4.0.0-{ts}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            subprocess.run(["git", "tag", f"v4-state-{ts}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", f"v4-state-{ts}"], cwd=self.repo)
        except: pass

if __name__ == "__main__":
    general = SwarmGeneral()
    if len(sys.argv) > 1 and sys.argv[1] == "AUTO_SYNC":
        general.sync_all()
    else:
        task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status Report"
        general.log("General", f"Executing Mission: {task}")
        leg = general.call_head("Hive_Legacy", f"Task: {task}")
        rec = general.call_head("Hive_Recovery", f"Task: {task}")
        with open(f"{general.repo}/RECOVERYLOGS.md", "a") as f:
            f.write(f"\n\n# 🐝 SWARM REPORT v4.0.0 [{time.ctime()}]\n\n## 🏛️ Hive Legacy\n{leg}\n\n## 🚑 Hive Recovery\n{rec}")
        general.sync_all()
