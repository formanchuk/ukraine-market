from flask import Flask, request
import telegram
import os

TOKEN = os.environ.get("BOT_TOKEN", "8935619238:AAG4rSiSWEsNM0NlX0fDivsZ6mWlhEN5ukg")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Ukraine Market Bot is running!'

@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        if update.message and update.message.text == '/start':
            user = update.message.from_user
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"🇺🇦 Вітаю, {user.first_name}!\n\n👇 Відкрийте магазин:",
                reply_markup={
                    "keyboard": [[{"text": "🚀 Відкрити Ukraine Market", "web_app": {"url": "https://formanchuk.github.io/ukraine-market-app/"}}]],
                    "resize_keyboard": True
                }
            )
        return 'ok', 200
    except Exception as e:
        print(e)
        return 'error', 500

if __name__ == '__main__':
    app.run()
