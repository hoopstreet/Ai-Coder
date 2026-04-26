import subprocess
import time

def start():
    print("🚀 Starting Ai-Coder Artic Singularity...")
    # Launch all modules
    subprocess.Popen(["python3", "/root/Ai-Coder/bot.py"])
    subprocess.Popen(["python3", "/root/Ai-Coder/core/sentinel.py"])
    subprocess.Popen(["python3", "/root/Ai-Coder/core/health_check.py"])
    
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    start()
