import sys
from agents.generators.vocab_generator import VocabularyPostGenerator
from agents.generators.grammar_generator import GrammarPostGenerator
from agents.generators.false_friend_generator import FalseFriendPostGenerator
from agents.review.post_judge import PostJudgeAgent
from helper_functions.category_loader import load_categories
from helper_functions.logger import log_dict_to_file
from helper_functions.topic_selector import TopicSelector
from storage.history import History
from storage.mongodb_handler import MongoDBHandler

SUPPORTED_TYPES = {
    "vocab": {
        "generator": VocabularyPostGenerator,
        "categories_path": "data/categories/vocabulary_categories.json",
        "history_path": "data/histories/vocab_history.json"
    },
    "grammar": {
        "generator": GrammarPostGenerator,
        "categories_path": "data/categories/grammar_categories.json",
        "history_path": "data/histories/grammar_history.json"
    },
    "false_friend": {
        "generator": FalseFriendPostGenerator,
        "categories_path": "data/categories/false_friend_categories.json",
        "history_path": "data/histories/false_friend_history.json"
    }
}


def generate_and_store_post(post_type: str, selector: TopicSelector, history: History) -> bool:
    try:
        topic = selector.get_unused_topic()
    except ValueError:
        print("⚠️ No unused topics available.")
        return False

    print(f"\n🔍 Selected topic: {topic}")

    generator_class = SUPPORTED_TYPES[post_type]["generator"]
    generator = generator_class()

    post = generator.run(topic)
    judge = PostJudgeAgent()
    judgment = judge.judge(post)

    if judgment["verdict"] == "accept":
        history.add_category(topic)

        try:
            db = MongoDBHandler(collection_name=f"{post_type}_posts")
            db.insert_post(post)
            print("✅ Post accepted and saved to MongoDB.")
        except Exception as e:
            print(f"⚠️ Failed to store post in MongoDB: {e}")
            return False

        print("#" * 20)
        return True
    else:
        print("❌ Post rejected:")
        print(f"Reason: {judgment['reason']}")
        log_dict_to_file(
            "logs/rejected_posts.log",
            {"topic": topic},
            post,
            judgment
        )
        print("#" * 100)
        return False


def run_generate(args):
    post_type = args.type.lower()
    count = args.count

    if post_type not in SUPPORTED_TYPES:
        print(f"❌ Unknown post type: {post_type}")
        sys.exit(1)

    print(f"📘 LexiLoop: Generating {count} {post_type} post(s)...")

    config = SUPPORTED_TYPES[post_type]
    categories = load_categories(config["categories_path"])
    history = History(config["history_path"])
    selector = TopicSelector(categories, history)

    success_count = 0
    for _ in range(count):
        if generate_and_store_post(post_type, selector, history):
            success_count += 1

    print(f"\n✅ Done: {success_count}/{count} post(s) successfully created and stored.")