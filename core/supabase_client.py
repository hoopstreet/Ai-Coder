import httpx
import os
import json

def get_config():
    # Helper to get env vars from the file
    env = {}
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env[k] = v.strip('"').strip("'")
    return env

CONF = get_config()
URL = CONF.get('SUPABASE_URL')
KEY = CONF.get('SUPABASE_KEY')

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_project(name):
    url = f"{URL}/rest/v1/projects?name=eq.{name}"
    with httpx.Client(headers=HEADERS) as client:
        resp = client.get(url)
        data = resp.json()
        return data[0] if data else None

def create_project(name, repo_url):
    url = f"{URL}/rest/v1/projects"
    payload = {"name": name, "repo_url": repo_url, "status": "active"}
    with httpx.Client(headers=HEADERS) as client:
        resp = client.post(url, json=payload)
        return resp.json()

def update_memory(project_id, memory_data):
    # Upsert logic for project_memory table
    url = f"{URL}/rest/v1/project_memory"
    # Using 'Prefer: resolution=merge-duplicates' style or simple POST
    payload = {"project_id": project_id, "data": memory_data}
    HEADERS_UPSERT = HEADERS.copy()
    HEADERS_UPSERT["Prefer"] = "resolution=merge-duplicates"
    
    with httpx.Client(headers=HEADERS_UPSERT) as client:
        resp = client.post(url, json=payload)
        return resp.status_code

def store_credential(project_id, key_name, value):
    url = f"{URL}/rest/v1/credentials"
    payload = {"project_id": project_id, "key": key_name, "value": value}
    with httpx.Client(headers=HEADERS) as client:
        resp = client.post(url, json=payload)
        return resp.status_code

if __name__ == "__main__":
    print("Testing Supabase Client...")
    proj = get_project("Ai-Coder")
    if proj:
        print(f"✅ Found Project: {proj['name']} (ID: {proj.get('id', 'N/A')})")
    else:
        print("❌ Project not found.")
