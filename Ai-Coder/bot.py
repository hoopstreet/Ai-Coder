import os
import time
import requests
import subprocess
from supabase import create_client

# Load Config
TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
CHAT_ID = 8296776401

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def execute_task(task_text):
    """Simple AI execution logic - expands as you add tools"""
    send_msg("⚙️ AI is processing your request on iPhone...")
    # This is where you can plug in 'interpreter' or custom python scripts
    try:
        # Example: Log task to Supabase if needed
        send_msg(f"✅ Task Received: {task_text}")
    except Exception as e:
        send_msg(f"❌ Error: {str(e)}")

def main():
    send_msg("🚀 Ai-Coder Bot is LIVE on iSH (iPhone)")
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 30}
            response = requests.get(url).json()
            
            for update in response.get("result", []):
                last_update_id = update["update_id"]
                if "message" in update and update["message"]["chat"]["id"] == CHAT_ID:
                    user_text = update["message"].get("text", "")
                    execute_task(user_text)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
