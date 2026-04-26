import os, requests, time

TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"

def send_msg(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": "6441584988", "text": text})

def main():
    print("🚀 Telegram Bot Controller Online")
    send_msg("🤖 AI-Coder: Enterprise System Online\nLocalhost: Ready for /Task")
    # Basic loop for updates would go here
    while True: time.sleep(10)

if __name__ == "__main__": main()
