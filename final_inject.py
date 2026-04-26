import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    project = "ai-coder"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Northflank Secret Group Schema requires an OBJECT for secrets, not an array
    secret_data = {
        "CHAT_ID": os.getenv("CHAT_ID"),
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
        "OR_KEY": os.getenv("OR_KEY"),
        "SB_URL": os.getenv("SB_URL"),
        "SB_KEY": os.getenv("SB_KEY"),
        "DOCKER_USER": os.getenv("DOCKER_USER"),
        "DOCKER_TOKEN": os.getenv("DOCKER_TOKEN"),
        "GEMINI_KEY": os.getenv("GEMINI_KEY")
    }

    # API Payload for Secret Group
    payload = {
        "name": "ai-coder-env",
        "description": "Ghost Protocol Environment Variables",
        "secretType": "environment",
        "priority": 10,
        "secrets": secret_data
    }

    print(f"📡 Injecting Validated Payload to Northflank...")
    url = f"https://api.northflank.com/v1/projects/{project}/secrets"
    
    # Check if exists (PUT) or create new (POST)
    r = requests.post(url, json=payload, headers=headers)
    
    if r.status_code == 409: # Already exists
        print("⚠️ Secret group exists, performing update...")
        r = requests.put(f"{url}/ai-coder-env", json=payload, headers=headers)

    if r.status_code < 300:
        print("✅ SUCCESS: Northflank Secret Group Synchronized.")
    else:
        print(f"❌ FAILED: {r.status_code} - {r.text}")

run()
