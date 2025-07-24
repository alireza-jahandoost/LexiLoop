import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("Missing TELEGRAM_TOKEN in .env")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    print("👤 User Info:")
    print(f"First name: {user.first_name}")
    print(f"Username: {user.username}")
    print(f"User ID: {user.id}")
    print(f"Chat ID: {chat.id}")
    print(f"Is private chat: {chat.type == 'private'}")

    await update.message.reply_text(f"👋 Hi {user.first_name}! Your user ID is:\n`{user.id}`", parse_mode="Markdown")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, handle_message))
    print("🤖 Bot is listening... Send it a message in Telegram.")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # This keeps it alive
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
