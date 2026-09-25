import os
import time
import requests
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running and active!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

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

def main_loop():
    print("Bot started with 4-token rotation system.")
    while True:
        token = get_next_token()
        time.sleep(60)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_flask)
    t.start()
    main_loop()
