import requests
import json
import base64
from core.rotator import SmartRotator

class CloudInfra:
    def __init__(self):
        self.rotator = SmartRotator()
        self.config = self.rotator.config
        self.nf_token = self.config.get("NORTHFLANK_TOKEN")
        self.docker = self.config.get("DOCKERHUB")

    def get_nf_headers(self):
        return {
            "Authorization": f"Bearer {self.nf_token}",
            "Content-Type": "application/json"
        }

    def list_projects(self):
        """Checks connection to Northflank."""
        url = "https://api.northflank.com/v1/projects"
        response = requests.get(url, headers=self.get_nf_headers())
        if response.status_code == 200:
            print("✅ Northflank Connection: Active")
            return response.json()
        else:
            print(f"❌ Northflank Error: {response.status_code}")
            return None

    def trigger_docker_build(self):
        """Logic for DockerHub integration."""
        print(f"🐳 Ready to push to: {self.docker['USERNAME']}/ai-coder")
        # Placeholder for docker-py or shell-out logic
        return True

if __name__ == "__main__":
    infra = CloudInfra()
    infra.list_projects()
