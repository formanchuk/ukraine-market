import os
import logging
from flask import Flask, request
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.environ.get("BOT_TOKEN", "8935619238:AAG4rSiSWEsNM0NlX0fDivsZ6mWlhEN5ukg")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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

# ========== ОБРОБНИКИ ==========
async def start(update: Update, context):
    user = update.effective_user
    await update.message.reply_text(
        f"🇺🇦 Вітаю, {user.first_name}!\n\n"
        f"**Ukraine Market** — ваш маркетплейс в Telegram\n\n"
        f"📦 Тут ви можете купувати та продавати товари\n"
        f"💼 Шукати роботу або працівників\n\n"
        f"📢 **Наші спільноти:**\n"
        f"• Канал з VIP оголошеннями: [Markets Ukraine](https://t.me/Markets_Ukraine)\n"
        f"• Група для відкритого спілкування: [MartekUA](https://t.me/MartekUA)\n\n"
        f"👇 Натисніть кнопку нижче, щоб відкрити магазин",
        parse_mode="Markdown",
        reply_markup=main_menu(),
        disable_web_page_preview=True
    )

async def web_app_data(update: Update, context):
    data = update.message.web_app_data
    if data:
        await update.message.reply_text(f"Отримано дані: {data.data}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("web_app_data", web_app_data))

# ========== ВЕБХУК ==========
@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def index():
    return "Ukraine Market Bot is running!"

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    app.run()
