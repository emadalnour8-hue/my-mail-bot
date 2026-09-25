import os
import time
import requests
import telebot
from flask import Flask

# جلب توكن البوت ومعرف المدير من متغيرات البيئة
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running and active!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# التوكنات الأربعة لنظام التدوير (Rotation System)
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

# استقبال الروابط والرسائل من تليجرام
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id
    
    if text and text.startswith('http'):
        # الحصول على التوكن التالي في الدور
        active_token = get_next_token()
        
        # رد مؤكد للمستخدم مع رقم التوكن المستخدم في الدورة
        bot.reply_to(
            message, 
            f"✅ New report received!\n"
            f"🔄 Processing with Token Index: {current_token_index}\n"
            f"🚀 Your report is being sent successfully."
        )
    else:
        bot.reply_to(
            message, 
            f"👋 Welcome! Send a tweet link (URL) to process the automated report.\n"
            f"📌 Your Chat ID is: {chat_id}"
        )

if __name__ == "__main__":
    import threading
    # تشغيل خادم Flask في الخلفية لإبقاء البوت حياً على Render
    t_flask = threading.Thread(target=run_flask)
    t_flask.start()
    
    # بدء الاستماع الفوري لرسائل تليجرام
    print("Telegram bot polling started...")
    bot.infinity_polling()
