import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TELEGRAM_TOKEN or not ADMIN_ID:
    raise RuntimeError("Missing TELEGRAM_TOKEN or ADMIN_ID in .env")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_message():
    try:
        message = "👋 Hello! This is a test message from your LexiLoop bot."
        await bot.send_message(chat_id=int(ADMIN_ID), text=message)
        print("✅ Message sent successfully to ADMIN_ID.")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

if __name__ == "__main__":
    asyncio.run(send_message())
