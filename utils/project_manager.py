import os
import json

def scan_local_projects(base_path="/root/Ai-Coder/projects/"):
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)
        print(f"📁 Created base projects directory at {base_path}")
        return []

    print(f"🔍 Scanning: {base_path}")
    projects = []
    
    try:
        for item in os.listdir(base_path):
            full_path = os.path.join(base_path, item)
            if os.path.isdir(full_path):
                has_dna = os.path.exists(os.path.join(full_path, "DNA.md"))
                projects.append({
                    "name": item,
                    "path": full_path,
                    "dna": has_dna
                })
        
        # Display Results
        print(f"{'PROJECT':<20} | {'DNA.md':<10}")
        print("-" * 35)
        for p in projects:
            status = "✅" if p['dna'] else "❌"
            print(f"{p['name']:<20} | {status:<10}")
            
    except Exception as e:
        print(f"❌ Scan Error: {e}")
    
    return projects

if __name__ == "__main__":
    scan_local_projects()
