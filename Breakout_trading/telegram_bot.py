# telegram_bot.py
from telegram import Bot

def send_signal(price, bot_token, chat_id):
    bot = Bot(token=bot_token)
    message = f"Dự đoán giá tiếp theo: {price}"
    bot.send_message(chat_id=chat_id, text=message)
