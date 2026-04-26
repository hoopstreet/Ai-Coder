import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    project = "ai-coder"
    service = "ai-coder"
    
    # We use the combined service config endpoint which handles both secrets and deployment settings
    url = f"https://api.northflank.com/v1/projects/{project}/services/combined/{service}/config"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    data = {
        "deployment": {
            "secrets": [
                {"key": "CHAT_ID", "value": os.getenv("CHAT_ID")},
                {"key": "TELEGRAM_TOKEN", "value": os.getenv("TELEGRAM_TOKEN")},
                {"key": "OR_KEY", "value": os.getenv("OR_KEY")},
                {"key": "SB_URL", "value": os.getenv("SB_URL")},
                {"key": "SB_KEY", "value": os.getenv("SB_KEY")},
                {"key": "DOCKER_USER", "value": os.getenv("DOCKER_USER")},
                {"key": "DOCKER_TOKEN", "value": os.getenv("DOCKER_TOKEN")},
                {"key": "GEMINI_KEY", "value": os.getenv("GEMINI_KEY")}
            ]
        }
    }
    
    print(f"📡 Force-injecting environment to {project}/{service}...")
    r = requests.put(url, json=data, headers=headers)
    if r.status_code < 300:
        print("✅ SUCCESS: Northflank Config Updated. Service should be live.")
    else:
        print(f"❌ Force Injection Failed: {r.status_code} - {r.text}")
        print("💡 Check if the 'Service ID' in your dashboard is exactly 'ai-coder'.")

run()
