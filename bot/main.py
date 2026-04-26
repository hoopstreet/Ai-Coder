import os, requests, time, subprocess

TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
CHAT_ID = "6441584988"

def send(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": text})

def get_updates(offset=None):
    try:
        r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params={"offset": offset, "timeout": 30})
        return r.json()
    except: return {"result": []}

def handle_command(cmd_text):
    print(f"📥 Telegram Trigger: {cmd_text}")
    # Forward entire string to Orchestrator
    process = subprocess.Popen(["python3", "/root/Ai-Coder/agent.py", cmd_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout if stdout else stderr

def main():
    send("⚡️ AI-CODER ENTERPRISE ONLINE\nPhase 3: File Injection Active\n\nCommands:\n/Select [name]\n/Add_Project [name] [url]\n/Task file:[name.py] [description]")
    offset = None
    while True:
        updates = get_updates(offset)
        for r in updates.get("result", []):
            offset = r["update_id"] + 1
            if "message" in r and "text" in r["message"]:
                msg = r["message"]["text"]
                if msg.startswith("/"):
                    # Clean the command and execute
                    clean_cmd = msg[1:]
                    response = handle_command(clean_cmd)
                    send(response)
        time.sleep(1)

if __name__ == "__main__": main()
