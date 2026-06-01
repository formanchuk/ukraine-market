from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

TOKEN = "8935619238:AAG4rSiSWEsNM0NlX0fDivsZ6mWlhEN5ukg"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========== КЛАВІАТУРА ==========
def main_menu():
    keyboard = [
        [KeyboardButton("🚀 Відкрити Ukraine Market", web_app=WebAppInfo(url="https://formanchuk.github.io/ukraine-market-app/"))],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ========== ОБРОБНИКИ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка даних з Web App (якщо потрібно)"""
    data = update.message.web_app_data
    if data:
        await update.message.reply_text(f"Отримано дані: {data.data}")

# ========== ЗАПУСК ==========
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    print("🚀 Ukraine Market Bot запущено!")
    print("✅ Єдина кнопка: Відкрити Ukraine Market")
    print("✅ Посилання: https://formanchuk.github.io/ukraine-market-app/")
    print("✅ Канал: https://t.me/Markets_Ukraine")
    print("✅ Група: https://t.me/MartekUA")
    
    app.run_polling()

if __name__ == "__main__":
    main()