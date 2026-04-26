import os, time, subprocess

def sync_to_github():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Autonomic Sync: {time.ctime()}"], check=True)
        subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
        print("🌍 GitHub Sync Complete.")
    except:
        pass

def main():
    print("📡 Swarm Sentinel v2.5.1: Monitoring & Auto-Push Active")
    while True:
        if os.path.exists('/root/Ai-Coder/master.log'):
            with open('/root/Ai-Coder/master.log', 'r') as f:
                log_data = f.read()
                if "❌" in log_data or "Failed" in log_data:
                    # Clear log and fix
                    open('/root/Ai-Coder/master.log', 'w').close()
                    subprocess.run(["agent", "SENTINEL_FIX: Resolve environmental conflicts and sync."])
                    sync_to_github()
        
        # Routine Sync every 60 seconds
        sync_to_github()
        time.sleep(60)

if __name__ == "__main__":
    main()
