import os, sys, requests, json, time, subprocess

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

    def log(self, msg):
        with open('master.log', 'a') as f:
            f.write(f"[{time.ctime()}] {msg}\n")
        print(f"🤖 {msg}")

    def auto_fix(self, error_msg):
        self.log(f"🛠 AUTO-RESOLVING: {error_msg[:50]}")
        # Self-correction logic: re-link paths and check environment
        subprocess.run(["hash", "-r"])
        if "FileNotFoundError" in error_msg:
            os.chdir("/root/Ai-Coder")
        return self.run("Finalize missing upgrades and merge code setup.")

    def run(self, task):
        self.log(f"Backtracking/Merging Task: {task}")
        # Version analysis loop simulation
        for key in self.gemini_keys:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": task}]}]}, timeout=20)
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            except: continue
        return "Failover mode active."

if __name__ == "__main__":
    agent = AutonomousAgent()
    if len(sys.argv) > 1:
        print(agent.run(" ".join(sys.argv[1:])))
