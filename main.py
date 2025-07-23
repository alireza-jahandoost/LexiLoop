import sys
from agents.generators.vocab_generator import VocabularyPostGenerator
from agents.review.post_judge import PostJudgeAgent
from helper_functions.category_loader import load_categories
from helper_functions.logger import log_dict_to_file
from helper_functions.topic_selector import TopicSelector
from storage.vocab_history import VocabHistory

from storage.mongodb_handler import MongoDBHandler


def main():
    print("📘 LexiLoop: Vocabulary Post Generator")

    # Load all vocab categories from JSON
    categories = load_categories("data/categories/vocabulary_categories.json")

    # Setup topic selection and history
    history = VocabHistory()
    selector = TopicSelector(categories, history)

    try:
        topic = selector.get_unused_topic()
    except ValueError:
        print("⚠️ No unused topics available.")
        sys.exit(1)

    print(f"🔍 Selected topic: {topic}")

    # Generate the post
    generator = VocabularyPostGenerator()
    post = generator.run(topic)

    # ✅ Run the judge
    judge = PostJudgeAgent()
    judgment = judge.judge(post)

    if judgment["verdict"] == "accept":
        # Store topic to history
        history.add_category(topic)
        print("\n✅ Post accepted:\n")

        # ✅ Save post in MongoDB
        try:
            db = MongoDBHandler(collection_name="vocab_posts")
            db.insert_post(post)
            print("📝 Post saved to MongoDB Atlas.")
        except Exception as e:
            print(f"⚠️ Failed to store post in MongoDB: {e}")


    else:
        print("\n❌ Post rejected:")
        print(f"Reason: {judgment['reason']}")

        log_dict_to_file(
            "logs/rejected_posts.log",
            {"topic": topic},
            post,
            judgment
        )
        sys.exit(1)


if __name__ == "__main__":
    main()