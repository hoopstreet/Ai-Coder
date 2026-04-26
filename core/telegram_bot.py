import httpx
import asyncio
import os
import subprocess

def get_env():
    env = {}
    path = '/root/Ai-Coder/.env'
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    env[k] = v.strip('"').strip("'")
    return env

ENV = get_env()
TOKEN = ENV.get('TELEGRAM_BOT_TOKEN')
API_URL = f"https://api.telegram.org/bot{TOKEN}"

async def send_msg(chat_id, text):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

async def main():
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env")
        return

    print("🤖 Telegram Bot is listening for /build commands...")
    offset = None
    
    while True:
        try:
            url = f"{API_URL}/getUpdates"
            if offset: url += f"?offset={offset}"
            
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=10.0)
                updates = resp.json().get("result", [])
                
                for update in updates:
                    offset = update["update_id"] + 1
                    msg = update.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "")

                    if text.startswith("/build "):
                        task = text.replace("/build ", "")
                        await send_msg(chat_id, f"🧬 Starting AI Orchestrator for: {task}")
                        
                        # Trigger the multi-key agent
                        proc = subprocess.run(
                            ["python3", "/root/Ai-Coder/agent.py", task],
                            capture_output=True, text=True
                        )
                        
                        result = proc.stdout if proc.stdout else proc.stderr
                        await send_msg(chat_id, f"✅ Result:\n{result[-500:]}")

            await asyncio.sleep(3)
        except Exception as e:
            print(f"Bot Error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
