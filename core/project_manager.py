import os, subprocess

class ProjectManager:
    def __init__(self):
        self.base_dir = "/root/Ai-Coder/projects"
        os.makedirs(self.base_dir, exist_ok=True)
        self.active_project = None

    def add_project(self, name, repo_url):
        path = os.path.join(self.base_dir, name)
        if os.path.exists(path):
            return f"Error: Project {name} already exists."
        
        # Fixed: Use capture_output=True for Python 3.9+
        process = subprocess.run(["git", "clone", repo_url, path], capture_output=True, text=True)
        
        if process.returncode != 0:
            return f"Failed to clone: {process.stderr}"

        dna_path = os.path.join(path, "DNA.md")
        if not os.path.exists(dna_path):
            with open(dna_path, "w") as f:
                f.write(f"# DNA: {name}\nInitialized via Ai-Coder Enterprise\n")
        
        return f"Project {name} cloned to {path}"

    def select_project(self, name):
        path = os.path.join(self.base_dir, name)
        if os.path.exists(path):
            self.active_project = name
            return f"Switched active project to: {name}"
        return f"Error: Project {name} not found."
