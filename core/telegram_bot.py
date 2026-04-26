import telebot
import subprocess
import os
import sys

TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Ai-Coder Bot Active. System is fully synced!")

@bot.message_handler(func=lambda message: True)
def handle_task(message):
    task = message.text
    bot.reply_to(message, f"🛠 Running: {task}")
    try:
        res = subprocess.check_output(["python3", "/root/Ai-Coder/agent.py", task], stderr=subprocess.STDOUT)
        bot.reply_to(message, f"✅ Result:\n{res.decode()[-1000:]}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🤖 Telegram Bot: Starting infinity polling...")
    sys.stdout.flush()
    bot.infinity_polling()
