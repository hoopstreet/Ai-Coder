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
    # Route Telegram commands to Agent CLI
    print(f"📥 Executing: {cmd_text}")
    process = subprocess.Popen(["python3", "/root/Ai-Coder/agent.py", cmd_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout if stdout else stderr

def main():
    send("🤖 AI-Coder: Enterprise Commander Online\nLocalhost: Connected to GitHub\nCommands: /Task, /Code, /Select")
    offset = None
    while True:
        updates = get_updates(offset)
        for r in updates.get("result", []):
            offset = r["update_id"] + 1
            if "message" in r and "text" in r["message"]:
                msg = r["message"]["text"]
                if msg.startswith("/"):
                    # Remove the slash and send to Agent
                    res = handle_command(msg[1:])
                    send(f"✅ Result:\n{res}")
        time.sleep(1)

if __name__ == "__main__": main()
