import os, requests, json, time

class GhostAgent:
    def __init__(self):
        self.creds = {
            "or": os.getenv("OR_KEY"),
            "sb": os.getenv("SB_KEY"),
            "sb_url": os.getenv("SB_URL"),
            "nf": os.getenv("NF_TOKEN")
        }
        self.gemini_keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas", "AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA"]

    def run(self):
        print("🔍 Scanning GitHub Repos...", flush=True)
        repos = [d for d in os.listdir('/root') if os.path.isdir(f'/root/{d}/.git')]
        
        print("🔍 Checking Cloud Status...", flush=True)
        infra = {"Supabase": "Offline", "Northflank": "Offline"}
        try:
            if requests.get(f"{self.creds['sb_url']}/rest/v1/", headers={"apikey": self.creds['sb'], "Authorization": f"Bearer {self.creds['sb']}"}, timeout=5).status_code < 400:
                infra["Supabase"] = "Online"
        except: pass
        try:
            r = requests.get("https://api.northflank.com/v1/projects", headers={"Authorization": f"Bearer {self.creds['nf']}"}, timeout=5)
            if r.status_code == 200: infra["Northflank"] = f"Online ({len(r.json().get('projects', []))} Proj)"
        except: pass

        with open("project_map.txt", "r") as f: mapping = f.read()

        prompt = f"AUDIT v3.0\nCloud: {json.dumps(infra)}\nGit Repos: {repos}\nFiles: {mapping[:800]}\nPlan deployment for GitHub to Northflank."
        
        print("🤖 Consulting AI failover cluster...", flush=True)
        headers = {"Authorization": f"Bearer {self.creds['or']}", "Content-Type": "application/json"}
        payload = {"model": "google/gemini-2.0-flash-001", "messages": [{"role": "user", "content": prompt}]}
        
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=40)
            print("\n" + "="*40 + "\n🚀 DEPLOYMENT READINESS REPORT\n" + "="*40)
            print(res.json()['choices'][0]['message']['content'])
        except:
            print("❌ AI link timed out. Check connection.")

if __name__ == "__main__":
    GhostAgent().run()
