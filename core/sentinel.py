import os, time, subprocess

def main():
    print("📡 Sentinel v2.6.1 Live: Monitoring Errors...")
    while True:
        # Check if master.log has a failure
        if os.path.exists('/root/Ai-Coder/master.log'):
            with open('/root/Ai-Coder/master.log', 'r') as f:
                if "❌" in f.read():
                    open('/root/Ai-Coder/master.log', 'w').close()
                    subprocess.run(["agent", "AUTONOMOUS_RECOVERY: Repair system state and sync memory."])
        
        # Periodic GitHub Sync every 2 minutes
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Routine Sync"])
        subprocess.run(["git", "push", "origin", "main", "--force"])
        time.sleep(120)

if __name__ == "__main__":
    main()
