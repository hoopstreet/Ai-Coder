import telebot
import subprocess
import os

TOKEN = "8162842268:AAFxPzIsbc3zg0CvSkzdf04OYR6UKgLfOY4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🚀 Ai-Coder Bot Active. Send me a task to build!")

@bot.message_handler(func=lambda message: True)
def handle_task(message):
    task = message.text
    bot.reply_to(message, f"🛠 Running task: {task}...")
    try:
        # Run the agent and capture output
        res = subprocess.check_output(["python3", "/root/Ai-Coder/agent.py", task], stderr=subprocess.STDOUT)
        bot.reply_to(message, f"✅ Done!\n{res.decode()[-500:]}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

print("🤖 Bot is starting...")
bot.infinity_polling()
