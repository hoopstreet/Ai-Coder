import os, json

class ProjectManager:
    def __init__(self):
        self.base_dir = "/root/Ai-Coder/projects"
        os.makedirs(self.base_dir, exist_ok=True)

    def list_projects(self):
        projects = [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]
        return projects

    def create_project(self, name, repo_url):
        path = os.path.join(self.base_dir, name)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "DNA.md"), "w") as f:
            f.write(f"# DNA: {name}\nGoal: {repo_url}\n")
        return path
