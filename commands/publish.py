import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from storage.mongodb_handler import MongoDBHandler

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
    bot = Bot(token=TELEGRAM_TOKEN)
else:
    bot = None

def add_hashtags(message: str, post_type: str) -> str:
    tags = {
        "vocab": "#vocabulary #vocabolario #wordsoftheday #paroledelgiorno",
        "grammar": "#grammar #grammatica",
        "false_friend": "#falsefriend #falsoamico"
    }
    return f"{message}\n\n{tags.get(post_type, '')}".strip()

async def run_publish(args):
    if not bot:
        raise RuntimeError("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID for publishing.")

    post_type = args.type.lower()

    if post_type not in ["vocab", "grammar", "false_friend"]:
        logger.error(f"Unsupported post type: {post_type}")
        return

    db = MongoDBHandler(collection_name=f"{post_type}_posts")
    query = {
        "type": post_type,
        "published": {"$ne": True}
    }

    post = db.find_post(query)

    if not post:
        logger.info(f"No unpublished '{post_type}' posts found.")
        return

    formatted_text = post.get("formatted_view", "").strip()
    if not formatted_text:
        logger.warning(f"Post {post.get('_id')} has no 'formatted_view'.")
        return

    message = add_hashtags(formatted_text, post_type)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")
    logger.info(f"Published '{post_type}' post: {post.get('_id')}")
    db.update_post({"_id": post["_id"]}, {"published": True})