import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Please set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in your .env file.")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_test_message():
    test_message = "✅ Test message from LexiLoop bot! If you see this, the connection works."
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=test_message)
        print("✅ Test message sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send test message: {e}")

if __name__ == "__main__":
    asyncio.run(send_test_message())