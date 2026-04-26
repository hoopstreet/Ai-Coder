import os

def get_config():
    env = {}
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env[k] = v.strip('"').strip("'")
    return env

conf = get_config()
URL = conf.get("SUPABASE_URL", "").rstrip('/')
KEY = conf.get("SUPABASE_SERVICE_ROLE", "")

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}
