import os
import json

# SUPABASE CONFIGURATION
URL = "https://your-project-id.supabase.co/rest/v1/vault"
# Note: HEADERS are usually generated with the API Key
HEADERS = {
    "apikey": "YOUR_SUPABASE_ANON_KEY",
    "Authorization": "Bearer YOUR_SUPABASE_ANON_KEY",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def get_config():
    """Helper to load local config/keys"""
    config_path = "/root/Ai-Coder/core/config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

print("✅ core/supabase_client.py: Repaired with HEADERS and URL.")
