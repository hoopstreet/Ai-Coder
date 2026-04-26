import os, requests, time, subprocess

# --- PROJECT CONFIG ---
TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
REPO_PATH = "/root/Ai-Coder"

def send_tg(msg):
    # Sends status updates back to your iPhone Telegram app
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    # Note: Replace 'YOUR_CHAT_ID' with your actual Telegram Chat ID if known
    # Or the bot will respond to the last person who messaged it.
    print(f"DEBUG: Sending to TG: {msg}")

def run_agent(task):
    print(f"🤖 AGENT STARTING: {task}")
    # This executes the /usr/bin/agent command we created earlier
    process = subprocess.Popen(["agent", task], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout if stdout else stderr

def main():
    print("🚀 Telegram Commander Active. Monitoring for /Code and /Select...")
    last_update = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            res = requests.get(url, params={"offset": last_update + 1}, timeout=30).json()
            
            for update in res.get("result", []):
                last_update = update["update_id"]
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")

                if not text: continue

                # COMMAND: /code <task>
                if text.startswith("/code"):
                    task = text.replace("/code", "").strip()
                    print(f"📥 Received Task: {task}")
                    # Run the CLI agent and get the result
                    output = run_agent(task)
                    # Send result back to Telegram
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                  data={"chat_id": chat_id, "text": f"✅ Execution Finished:\n{output}"})

                # COMMAND: /select <project>
                elif text.startswith("/select"):
                    project_name = text.replace("/select", "").strip()
                    # Logic to switch project context
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                  data={"chat_id": chat_id, "text": f"📂 Switched to: {project_name}. successfully what is next?"})

            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
