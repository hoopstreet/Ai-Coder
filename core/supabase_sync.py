import os
from supabase import create_client

URL = "https://ixdukafvxqermhgoczou.supabase.co/"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M iOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91 Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3M iwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1 LF3RJnQNacBc-dHk"

def sync_state(msg):
    try:
        client = create_client(URL, KEY)
        client.table("logs").insert({"level": "INFO", "module": "SYNC", "message": msg}).execute()
        client.table("projects").upsert({"name": "Ai-Coder", "status": "active", "roadmap_version": "v2.2.0"}).execute()
    except Exception as e:
        print(f"Sync Error: {e}")

if __name__ == "__main__":
    sync_state("Manual Sync Triggered")
