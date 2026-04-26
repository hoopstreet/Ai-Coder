import os, time, subprocess

def main():
    print("📡 Swarm Sentinel v2.4.1: ACTIVE (24/7 Real-time)")
    while True:
        if os.path.exists('master.log'):
            with open('master.log', 'r') as f:
                content = f.read()
                if "❌" in content or "Failed" in content:
                    # Clean log and trigger auto-recovery
                    open('master.log', 'w').close() 
                    subprocess.run(["agent", "AUTONOMOUS_FIX: Analyze master.log failures and restore system integrity."])
        time.sleep(5)

if __name__ == "__main__":
    main()
