import os, requests, subprocess, time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", 0))

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg[:4000]}
    )

def run_ai(task):
    cmd = f"""
interpreter <<EOF
You are a senior AI developer.

TASK:
{task}

DO:
- Plan
- Code
- Test
- Fix errors
- Save files

Then:
git add .
git commit -m "auto: AI update"
git push origin main
EOF
"""
    subprocess.run(cmd, shell=True)

def main():
    send("🤖 AI Dev Bot Running (Northflank)")

    offset = None

    while True:
        r = requests.get(
            f"https://api.telegram.org/bot{TOKEN}/getUpdates",
            params={"offset": offset, "timeout": 100}
        ).json()

        for u in r.get("result", []):
            offset = u["update_id"] + 1

            msg = u["message"]["text"]
            chat = u["message"]["chat"]["id"]

            if chat != CHAT_ID:
                continue

            send("⚙️ Processing...")
            run_ai(msg)
            send("✅ Done + pushed")

        time.sleep(2)

if __name__ == "__main__":
    main()
