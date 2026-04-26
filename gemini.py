import os, sys, requests, json, time, subprocess

class SwarmBrain:
    def __init__(self):
        self.repo = "/root/Ai-Coder"
        self.keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas", "AIzaSyBRmOlHL4NZ5k_8mOKFvO6QwIs83KtkTxA", "AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY", "AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg", "AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]
        self.or_key = "sk-or-v1-d44bb63c9aeebdlbd139026679ee75c3077322c75e02615200367c49ecb4d11"
        self.models = ["google/gemini-2.0-flash-lite-preview-02-05:free", "deepseek/deepseek-r1:free", "google/gemini-2.0-flash-001"]

    def log(self, msg):
        with open(f"{self.repo}/master.log", "a") as f: f.write(f"[{time.ctime()}] {msg}\n")
        print(f"🤖 {msg}")

    def sync(self):
        try:
            ts = int(time.time())
            tag = f"v2.9.1-state-{ts}"
            subprocess.run(["git", "add", "."], cwd=self.repo)
            subprocess.run(["git", "commit", "-m", f"Autonomic Sync {tag}"], cwd=self.repo)
            subprocess.run(["git", "push", "origin", "main", "--force"], cwd=self.repo)
            subprocess.run(["git", "tag", tag], cwd=self.repo)
            subprocess.run(["git", "push", "origin", tag], cwd=self.repo)
            self.log(f"🌍 Cloud Mirror & Tag Sync: {tag}")
        except: pass

    def ask(self, task):
        for k in self.keys:
            try:
                r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}", json={"contents": [{"parts": [{"text": task}]}]}, timeout=15)
                if r.status_code == 200: return r.json()['candidates'][0]['content']['parts'][0]['text']
            except: continue
        for m in self.models:
            try:
                r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {self.or_key}"}, json={"model": m, "messages": [{"role": "user", "content": task}]}, timeout=30)
                if r.status_code == 200: return r.json()['choices'][0]['message']['content']
            except: continue
        return None

if __name__ == "__main__":
    brain = SwarmBrain()
    if len(sys.argv) > 1:
        if sys.argv[1] == "AUTO_SYNC": brain.sync()
        else:
            res = brain.ask(" ".join(sys.argv[1:]))
            if res:
                with open(f"{brain.repo}/RECOVERYLOGS.md", "a") as f: f.write(f"\n\n### [MERGE {time.ctime()}]\n{res}")
                brain.sync()
