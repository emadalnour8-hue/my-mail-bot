import os
import time
import requests
import threading
from flask import Flask, request

app = Flask('')

@app.route('/')
def home():
    return "Bot is running and active!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# قراءة التوكنات الأربعة ومعرف المدير من المتغيرات البيئية
tokens = [
    os.getenv('TWITTER_TOKEN_1'),
    os.getenv('TWITTER_TOKEN_2'),
    os.getenv('TWITTER_TOKEN_3'),
    os.getenv('TWITTER_TOKEN_4']

ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID', '8081542687')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') # إذا كان البوت يدار عبر تليجرام بوت

current_token_index = 0

def get_next_token():
    global current_token_index
    token = tokens[current_token_index]
    current_token_index = (current_token_index + 1) % len(tokens)
    return token

def send_telegram_message(chat_id, text):
    if not TELEGRAM_BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

# مسار لاستقبال التحديثات من تليجرام (Webhook) أو استقبال الروابط
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if data and 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text.startswith('http'):
            token = get_next_token()
            # محاكاة إرسال البلاغ باستخدام التوكن الحالي
            send_telegram_message(chat_id, f"New report received!\nProcessing URL with token index: {current_token_index}\nYour report was sent.")
            
    return "OK", 200

if __name__ == "__main__":
    # تشغيل خادم الويب Flask في خيط منفصل لإبقاء الخدمة حية على Render
    t = threading.Thread(target=run_flask)
    t.start()
