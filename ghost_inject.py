import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    project = "ai-coder"
    service = "ai-coder"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Payload covering all your credentials
    secrets = [
        {"key": "CHAT_ID", "value": os.getenv("CHAT_ID")},
        {"key": "TELEGRAM_TOKEN", "value": os.getenv("TELEGRAM_TOKEN")},
        {"key": "OR_KEY", "value": os.getenv("OR_KEY")},
        {"key": "SB_URL", "value": os.getenv("SB_URL")},
        {"key": "SB_KEY", "value": os.getenv("SB_KEY")},
        {"key": "DOCKER_USER", "value": os.getenv("DOCKER_USER")},
        {"key": "DOCKER_TOKEN", "value": os.getenv("DOCKER_TOKEN")},
        {"key": "GEMINI_KEY", "value": os.getenv("GEMINI_KEY")}
    ]

    # Try Deployment Config Path
    url_deploy = f"https://api.northflank.com/v1/projects/{project}/services/deployment/{service}/config"
    print(f"📡 Attempting Ghost-Injection (Path: Deployment)...")
    r = requests.put(url_deploy, json={"deployment": {"secrets": secrets}}, headers=headers)
    
    if r.status_code < 300:
        print("✅ SUCCESS: Northflank Deployment Updated.")
        return

    # Try Secret Groups Path (Alternative if service path 404s)
    print(f"⚠️ Deployment Path failed ({r.status_code}). Attempting Secret Group override...")
    url_secret = f"https://api.northflank.com/v1/projects/{project}/secrets"
    # Note: Secret groups usually require a name/link, this is a simplified global push
    r_sec = requests.post(url_secret, json={"name": "ai-coder-secrets", "secrets": secrets}, headers=headers)
    
    if r_sec.status_code < 300:
         print("✅ SUCCESS: Secret Group created/updated.")
    else:
         print(f"❌ CRITICAL: Injection failed. Final Status: {r_sec.status_code}")
         print(f"Error Log: {r_sec.text}")

run()
