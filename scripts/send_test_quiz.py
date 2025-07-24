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

async def send_quiz():
    question = "Which of these is an Italian modal verb?"
    options = ["cane", "mangiare", "potere", "rosso"]
    correct_option_id = 2  # "potere"

    try:
        await bot.send_poll(
            chat_id=TELEGRAM_CHAT_ID,
            question=question,
            options=options,
            type="quiz",
            correct_option_id=correct_option_id,
            is_anonymous=True,
            explanation="✅ 'Potere' means 'to be able to' – it's a modal verb like 'can'.",
        )
        print("✅ Quiz sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send quiz: {e}")

if __name__ == "__main__":
    asyncio.run(send_quiz())
