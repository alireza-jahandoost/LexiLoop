import sys
from argparse import Namespace
from storage.mongodb_handler import MongoDBHandler
from commands.generate import run_generate  # ✅ reuses your existing generator
from commands.generate import SUPPORTED_TYPES  # reuse config mapping if available

def run_maintain(args):
    threshold = args.threshold
    count = args.count
    types = args.types or list(SUPPORTED_TYPES.keys())

    print(f"🔧 Maintaining post buffers (threshold = {threshold}, count = {count})...")

    for post_type in types:
        if post_type not in SUPPORTED_TYPES:
            print(f"❌ Unsupported post type: {post_type}")
            continue

        db = MongoDBHandler(collection_name=f"{post_type}_posts")
        current_unpublished = db.collection.count_documents({"published": {"$ne": True}})
        print(f"📊 {post_type}: {current_unpublished} unpublished post(s)")

        if current_unpublished >= threshold:
            print(f"✅ {post_type} buffer is sufficient.\n")
            continue

        print(f"🚀 Generating {count} new {post_type} post(s)...")
        gen_args = Namespace(type=post_type, count=count)
        run_generate(gen_args)