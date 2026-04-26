import httpx, os

class SupabaseClient:
    def __init__(self):
        self.url = "https://ixdukafvxqermhgoczou.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4ZHVrYWZ2eHFlcm1oZ29jem91Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTc1MjM3MiwiZXhwIjoyMDkxMzI4MzcyfQ.R4syxxjfZNKRlMtCfOHpY-XMwZ1LF3RJnQNacBc-dHk"
        self.headers = {"apikey": self.key, "Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}

    def log_task(self, project_name, task, status):
        data = {"project_name": project_name, "task": task, "status": status}
        try:
            return httpx.post(f"{self.url}/rest/v1/tasks", headers=self.headers, json=data)
        except: return None
