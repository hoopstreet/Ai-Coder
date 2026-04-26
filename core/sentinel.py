import time, subprocess
while True:
    subprocess.run(["python3", "/root/Ai-Coder/gemini.py", "AUTO_SYNC"])
    time.sleep(60)
