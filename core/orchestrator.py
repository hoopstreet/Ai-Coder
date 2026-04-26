import os, sys, time, subprocess
from core.ai_brain import GeminiBrain
from core.project_manager import ProjectManager
from core.supabase_client import SupabaseClient

class AgentCLI:
    def __init__(self):
        self.spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.brain = GeminiBrain()
        self.pm = ProjectManager()
        self.db = SupabaseClient()
    
    def loading(self, msg, duration=1):
        end = time.time() + duration
        i = 0
        while time.time() < end:
            sys.stdout.write(f"\r{self.spinner[i % len(self.spinner)]} {msg}...")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        print(f"\r✅ {msg} Done!")

    def execute(self, task):
        # Handle /Add_Project name repo_url
        if task.startswith("Add_Project"):
            parts = task.split(" ")
            if len(parts) < 3: return "Usage: Add_Project [name] [repo_url]"
            self.loading(f"Cloning {parts[1]}")
            return self.pm.add_project(parts[1], parts[2])

        # Handle /Select name
        if task.startswith("Select"):
            parts = task.split(" ")
            if len(parts) < 2: return "Usage: Select [name]"
            return self.pm.select_project(parts[1])

        # Default Pipeline Logic
        if not self.pm.active_project:
            return "⚠️ No project selected. Use /Select first."

        self.loading(f"Processing Task for {self.pm.active_project}")
        self.db.log_task(self.pm.active_project, task, "In Progress")
        
        # Simulated Agent Pipeline (v1.3)
        self.loading("Analyzing Repo Structure", duration=2)
        version = f"v1.3.{int(time.time()) % 1000}"
        
        # DNA update logic for isolated project
        dna_path = f"/root/Ai-Coder/projects/{self.pm.active_project}/DNA.md"
        with open(dna_path, "a") as f:
            f.write(f"\n[{version}] - Task: {task}\n")

        self.db.log_task(self.pm.active_project, task, "Completed")
        return f"🚀 Success: {task} | Project: {self.pm.active_project} | Version: {version}"

if __name__ == "__main__":
    agent = AgentCLI()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Initialize"
    print(agent.execute(task))
