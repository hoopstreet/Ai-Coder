import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env manually
env_path = '/root/Ai-Coder/.env'
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                os.environ[k] = v.strip('"')

TOKEN = os.environ.get('TELEGRAM_TOKEN')

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text('🤖 **Ai-Coder Pro Active**\n/task - View Roadmap')

async def task(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text('🗺 **Project Roadmap**\n1. ✅ Foundational CLI\n2. ⏳ GitHub Sync\n3. ⏳ Supabase Integration')

if __name__ == '__main__':
    if not TOKEN:
        print('❌ Critical Error: TELEGRAM_TOKEN not found in environment.')
    else:
        print(f'✅ Token Loaded: {TOKEN[:10]}...')
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('task', task))
        print('🚀 Commander online. Waiting for messages...')
        app.run_polling()
