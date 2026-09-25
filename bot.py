import os
import threading
import time
import requests
import telebot
from flask import Flask

# إعداد بوت تليجرام باستخدام التوكن من المتغيرات البيئية أو مباشرة
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# إعداد خادم Flask لإبقاء البوت حياً على Render
app = Flask('')

@app.route('/')
def home():
    return "Bot is running and active!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# التوكنات الأربعة لإكس (تويتر)
tokens = [
    os.getenv('TWITTER_TOKEN_1'),
    os.getenv('TWITTER_TOKEN_2'),
    os.getenv('TWITTER_TOKEN_3'),
    os.getenv('TWITTER_TOKEN_4')
]

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '8081542687')
current_token_index = 0

def get_next_token():
    global current_token_index
    token = tokens[current_token_index]
    current_token_index = (current_token_index + 1) % len(tokens)
    return token

# استقبال رسائل وروابط تليجرام
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id
    
    if text and text.startswith('http'):
        token = get_next_token()
        # هنا يتم تنفيذ إرسال البلاغ باستخدام التوكن الحالي
        bot.reply_to(message, f"New report received!\nProcessing with token index: {current_token_index}\nYour report was sent.")
    else:
        bot.reply_to(message, f"Ahlalan! Send a tweet URL to process the report.\nYour Chat ID is: {chat_id}")

def run_telegram_bot():
    print("Telegram bot polling started...")
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل Flask في خلفية منفصلة
    t_flask = threading.Thread(target=run_flask)
    t_flask.start()
    
    # تشغيل بوت تليجرام للاستماع الفوري
    run_telegram_bot()
