import os
import asyncio
import httpx
import json
import subprocess
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from supabase import create_client, Client

# --- LOAD ENVIRONMENT ---
env_path = '/root/Ai-Coder/.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                os.environ[k] = v.strip('"').strip("'")

TOKEN = os.environ.get('TELEGRAM_TOKEN')
SB_URL = os.environ.get('SUPABASE_URL')
SB_KEY = os.environ.get('SUPABASE_KEY')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

supabase: Client = create_client(SB_URL, SB_KEY) if SB_URL and SB_KEY else None

async def ask_gemini(prompt: str, context: str = ""):
    # FIXED URL LINE
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"SYSTEM: Senior Dev. Context: {context}\nRequest: {prompt}"}]}]}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(url, json=payload, timeout=30.0)
            data = r.json()
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("🏢 **Agent CLI Online**\n/code <task>\n/select <project>")

async def code_task(u: Update, c: ContextTypes.DEFAULT_TYPE):
    task = " ".join(c.args)
    if not task:
        await u.message.reply_text("Usage: /code <task>")
        return
    await u.message.reply_text("🧬 **Agent CLI: Processing...** ⏳")
    resp = await ask_gemini(task, "Enterprise Multi-Project")
    version = f"v1.0.{int(datetime.now().timestamp()) % 1000}"
    os.makedirs("/root/Ai-Coder/dna", exist_ok=True)
    with open("/root/Ai-Coder/dna/DNA.md", "a") as f:
        f.write(f"\n## [{version}] - {datetime.now()}\nTask: {task}\n")
    await u.message.reply_text(f"✅ **Done: {version}**\n\n{resp[:4000]}")

if __name__ == '__main__':
    print('🚀 Agent CLI is starting (Fixed URL)...')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('code', code_task))
    app.run_polling()
