import os, sys, json, httpx, asyncio, subprocess, re

def get_config():
    env = {}
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

conf = get_config()
OR_KEY = conf.get("OPENROUTER_KEY")

def clean_json(text):
    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*|\s*```', '', text)
    # Fix common escape errors
    return text.strip()

async def call_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": f"Return ONLY a JSON object with 'thought' and 'files' (list of {{path, content}}). Task: {prompt}"}]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(url, json=payload, headers=headers)
        data = r.json()
        raw_content = data['choices'][0]['message']['content']
        try:
            return json.loads(clean_json(raw_content))
        except:
            # Fallback for broken JSON: Try to extract everything between first { and last }
            match = re.search(r'(\{.*\})', raw_content, re.DOTALL)
            if match: return json.loads(match.group(1))
            raise

async def main():
    if len(sys.argv) < 2: return
    task = sys.argv[1]
    print(f"🧠 Processing: {task}")
    try:
        res = await call_openrouter(task)
        for file in res.get('files', []):
            os.makedirs(os.path.dirname(file['path']), exist_ok=True)
            with open(file['path'], 'w') as f:
                f.write(file['content'])
            print(f"💾 Saved {file['path']}")
        
        # Auto-Git Sync
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"feat: {task}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 GitHub Sync Complete")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
