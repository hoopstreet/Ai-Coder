import telebot
import subprocess
import os

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token.  DO NOT hardcode the token directly in the code.
# Instead, retrieve it from an environment variable or a secure configuration file.
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') # Example: Read token from environment variable

if not BOT_TOKEN:
    raise ValueError("Telegram bot token not found.  Please set the TELEGRAM_BOT_TOKEN environment variable.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that can run tasks. Send me a task to execute.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    task = message.text
    bot.reply_to(message, "Executing task...")

    try:
        # Safely construct the command to execute agent.py with the user's task.
        # Consider using shlex.quote to properly escape the task string for shell execution if needed.
        command = ['python', 'agent.py', task]

        # Execute the command, capturing both stdout and stderr.
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decode the output from bytes to string.
        stdout_str = stdout.decode('utf-8')
        stderr_str = stderr.decode('utf-8')

        # Construct the reply message.
        reply = f"Task completed.\nStdout:\n{stdout_str}\nStderr:\n{stderr_str}"

        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"Error executing task: {str(e)}")

if __name__ == "__main__":
    print("Starting Telegram bot...")
    bot.infinity_polling()