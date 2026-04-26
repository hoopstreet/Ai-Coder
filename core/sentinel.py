import os, time, subprocess

def main():
    print("📡 Sentinel v2.7.0: NO-HUMAN Mode Active")
    while True:
        # 1. Check for system pain (master.log errors)
        if os.path.exists('/root/Ai-Coder/master.log'):
            with open('/root/Ai-Coder/master.log', 'r') as f:
                if "❌" in f.read():
                    open('/root/Ai-Coder/master.log', 'w').close()
                    subprocess.run(["python3", "/root/Ai-Coder/gemini.py", "REPAIR_AND_MERGE"])
        
        # 2. Forced Full Sync every 60 seconds
        subprocess.run(["python3", "/root/Ai-Coder/gemini.py", "AUTO_SYNC"])
        time.sleep(60)

if __name__ == "__main__":
    main()
