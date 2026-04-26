import os, sys, time
from core.ai_brain import GeminiBrain
from core.project_manager import ProjectManager
from core.supabase_client import SupabaseClient
from core.injector import FileInjector

class AgentCLI:
    def __init__(self):
        self.brain = GeminiBrain()
        self.pm = ProjectManager()
        self.db = SupabaseClient()
        self.injector = FileInjector()
    
    def execute(self, task):
        if task.startswith("Add_Project") or task.startswith("Select"):
            # (Project management logic remains same)
            import subprocess
            if task.startswith("Add_Project"):
                parts = task.split(" ")
                return self.pm.add_project(parts[1], parts[2])
            return self.pm.select_project(task.split(" ")[1])

        if not self.pm.active_project:
            return "⚠️ No project selected."

        project_path = os.path.join(self.pm.base_dir, self.pm.active_project)
        
        # REAL PHASE 3 WORKFLOW
        print(f"🧠 Gemini thinking: {task}")
        code = self.brain.generate_code(task, context=f"Project: {self.pm.active_project}")
        
        # Simple heuristic: if task contains a filename, inject it
        filename = "generated_logic.py"
        if "file:" in task.lower():
            filename = task.lower().split("file:")[1].split(" ")[0]

        res = self.injector.inject(project_path, filename, code)
        self.db.log_task(self.pm.active_project, task, "Completed")
        
        return f"🚀 {res}\n📦 Version: v1.3.1\n🔗 Logged to Supabase"

if __name__ == "__main__":
    agent = AgentCLI()
    print(agent.execute(" ".join(sys.argv[1:])))
