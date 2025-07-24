import os
import asyncio
from dotenv import load_dotenv
from storage.mongodb_handler import MongoDBHandler
from telegram import Bot

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

POST_TYPES = ["vocab", "grammar", "false_friend"]
MIN_GOOD = 5

if not TELEGRAM_TOKEN or not ADMIN_ID:
    raise RuntimeError("Missing TELEGRAM_TOKEN or ADMIN_ID in .env")

bot = Bot(token=TELEGRAM_TOKEN)

async def run_check(args):
    lines = ["📦 *Post Buffer Status*"]
    good = True

    for post_type in POST_TYPES:
        db = MongoDBHandler(collection_name=f"{post_type}_posts")
        count = db.collection.count_documents({"published": {"$ne": True}})
        status = "✅" if count >= MIN_GOOD else "❌"
        if count < MIN_GOOD:
            good = False
        lines.append(f"{status} *{post_type}*: {count} unpublished")

    summary = "\n".join(lines)

    try:
        await bot.send_message(chat_id=int(ADMIN_ID), text=summary, parse_mode="Markdown")
        print("📬 Status sent to admin.")
    except Exception as e:
        print(f"❌ Failed to send status to admin: {e}")
