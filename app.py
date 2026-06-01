import os
import logging
from flask import Flask, request
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Dispatcher, CommandHandler

# Налаштування логування, щоб бачити помилки в логах Render
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8935619238:AAG4rSiSWEsNM0NlX0fDivsZ6mWlhEN5ukg")

# ========== Flask-додаток ==========
app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# ========== КЛАВІАТУРА ==========
def main_menu():
    keyboard = [
        [KeyboardButton("🚀 Відкрити Ukraine Market", web_app=WebAppInfo(url="https://formanchuk.github.io/ukraine-market-app/"))],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ========== ОБРОБНИКИ (синхронні, для сумісності) ==========
def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(
        f"🇺🇦 Вітаю, {user.first_name}!\n\n"
        f"**Ukraine Market** — ваш маркетплейс в Telegram\n\n"
        f"👇 Натисніть кнопку нижче, щоб відкрити магазин",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

dispatcher.add_handler(CommandHandler("start", start))

# ========== ВЕБХУК ==========
@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok', 200
    except Exception as e:
        logger.error(f"Помилка в webhook: {e}")
        return 'error', 500

@app.route('/')
def index():
    return "Ukraine Market Bot is running!"

# Цей блок не використовується Gunicorn, але потрібен для локального тестування
if __name__ == '__main__':
    app.run()
