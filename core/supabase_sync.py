import httpx
import sys
from core.supabase_client import HEADERS, URL, get_config

def sync_vault():
    conf = get_config()
    creds = [
        {"project_name": "Ai-Coder", "key_name": "GITHUB_TOKEN", "encrypted_value": conf.get("GITHUB_TOKEN")},
        {"project_name": "Ai-Coder", "key_name": "TELEGRAM_TOKEN", "encrypted_value": conf.get("TELEGRAM_BOT_TOKEN")},
        {"project_name": "Ai-Coder", "key_name": "OPENROUTER_KEY", "encrypted_value": conf.get("OPENROUTER_KEY")}
    ]
    
    print(f"🚀 Initiating Cloud Sync for {len(creds)} keys...")
    
    # Filter out None values
    valid_creds = [c for c in creds if c["encrypted_value"]]
    
    try:
        with httpx.Client() as client:
            # We use upsert logic (Prefer: resolution=merge)
            response = client.post(URL, json=valid_creds, headers=HEADERS)
            if response.status_code in [200, 201]:
                print("✅ CLOUD SYNC SUCCESSFUL: Vault updated.")
            else:
                print(f"⚠️ CLOUD SYNC ISSUE: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ TRANSPORT ERROR: {e}")

if __name__ == "__main__":
    sync_vault()
