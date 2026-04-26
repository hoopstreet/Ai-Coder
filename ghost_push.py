import requests, os

def run():
    token = os.getenv("NF_TOKEN")
    # Project and Service IDs derived from your URL
    project = "ai-coder"
    service = "ai-coder"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # 1. Create/Update a Secret Group
    secret_payload = {
        "name": "ghost-credentials",
        "description": "Ghost Protocol credentials managed by AI-Coder",
        "secretType": "environment",
        "priority": 100,
        "secrets": {
            "CHAT_ID": os.getenv("CHAT_ID"),
            "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
            "OR_KEY": os.getenv("OR_KEY"),
            "SB_URL": os.getenv("SB_URL"),
            "SB_KEY": os.getenv("SB_KEY"),
            "DOCKER_USER": os.getenv("DOCKER_USER"),
            "DOCKER_TOKEN": os.getenv("DOCKER_TOKEN"),
            "GEMINI_KEY": os.getenv("GEMINI_KEY")
        }
    }

    url_sec = f"https://api.northflank.com/v1/projects/{project}/secrets"
    print(f"📡 Syncing Secret Group...")
    r = requests.post(url_sec, json=secret_payload, headers=headers)
    
    if r.status_code == 409: # Conflict means it exists
        requests.put(f"{url_sec}/ghost-credentials", json=secret_payload, headers=headers)
        print("✅ Secret Group Updated.")
    elif r.status_code < 300:
        print("✅ Secret Group Created.")
    else:
        print(f"❌ Secret Group Error: {r.status_code} - {r.text}")

    # 2. Link Secret Group to the Deployment
    # This ensures the service actually HAS access to these variables
    url_link = f"https://api.northflank.com/v1/projects/{project}/services/deployment/{service}/config"
    link_payload = {
        "deployment": {
            "externalSecrets": [
                {"secretGroupId": "ghost-credentials"}
            ]
        }
    }
    print(f"🔗 Linking Secret Group to Service...")
    r_link = requests.put(url_link, json=link_payload, headers=headers)
    if r_link.status_code < 300:
        print("🚀 SUCCESS: Ghost Protocol active on Northflank.")
    else:
        print(f"⚠️ Linking Warning: {r_link.status_code} - {r_link.text}")

run()
