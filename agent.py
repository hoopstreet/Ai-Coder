import os, sys, httpx, asyncio, json, random, subprocess
from datetime import datetime

def load_env():
    env = {}
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env[k] = v.strip('"').strip("'")
    return env

ENV = load_env()
GEMINI_KEYS = [ENV.get(f"GEMINI_KEY_{i}") for i in range(1, 6) if ENV.get(f"GEMINI_KEY_{i}")]
OR_KEY = ENV.get("OPENROUTER_KEY")

async def call_openrouter(prompt):
    print("🔄 Switching to OpenRouter Fallback...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "system", "content": "Output JSON: {\"explanation\":\"\",\"files\":[{\"path\":\"\",\"content\":\"\"}]}"},
                     {"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=60.0)
        data = resp.json()
        return json.loads(data['choices'][0]['message']['content'])

async def call_ai(prompt, pro_mode=False):
    model = "gemini-2.0-pro-exp-02-05" if pro_mode else "gemini-2.0-flash"
    shuffled_keys = list(GEMINI_KEYS)
    random.shuffle(shuffled_keys)
    for key in shuffled_keys:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}], "systemInstruction": {"parts": [{"text": "Output JSON: {\"explanation\":\"\",\"files\":[{\"path\":\"\",\"content\":\"\"}]}"}]}, "generationConfig": {"responseMimeType": "application/json"}}
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload, timeout=30.0)
                if resp.status_code == 200: return json.loads(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            except: continue
    # If all Gemini fail, use OpenRouter
    if OR_KEY: return await call_openrouter(prompt)
    return {"error": "All providers exhausted."}

def github_sync(task):
    try:
        version = datetime.now().strftime("v%y.%m%d.%H%M")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"feat: {task} ({version})"], check=True)
        subprocess.run(["git", "tag", version], check=True)
        subprocess.run(["git", "push", "origin", "main", "--tags"], check=True)
        print(f"🚀 GitHub Sync Complete ({version})")
    except Exception as e: print(f"⚠️ Git Error: {e}")

async def main():
    if len(sys.argv) < 2: return
    task = sys.argv[1]
    res = await call_ai(task, "--pro" in sys.argv)
    if "error" in res:
        print(f"❌ {res['error']}")
        return
    for f in res.get("files", []):
        path = os.path.join("/root/Ai-Coder", f["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file: file.write(f["content"])
        print(f"💾 Saved {f['path']}")
    github_sync(task)

if __name__ == "__main__":
    asyncio.run(main())
