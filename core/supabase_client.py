import os

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
URL = conf.get("SUPABASE_URL", "").rstrip('/')
# Priority to service role for bypassing RLS
KEY = conf.get("SUPABASE_SERVICE_ROLE") or conf.get("SUPABASE_KEY")

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}
