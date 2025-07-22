# main.py

import json
import sys
from pathlib import Path

from agents.generators.vocab_generator import VocabularyPostGenerator
from helper_functions.topic_selector import TopicSelector
from storage.vocab_history import VocabHistory


def load_vocab_categories(path: str) -> list[str]:
    full_path = Path(__file__).resolve().parent / path
    if not full_path.exists():
        print(f"❌ Category file not found: {full_path}")
        sys.exit(1)

    with open(full_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [entry["category"] for entry in data if "category" in entry]
        except json.JSONDecodeError:
            print(f"❌ Failed to parse JSON file: {full_path}")
            sys.exit(1)


def main():
    print("📘 LexiLoop: Vocabulary Post Generator")

    # Load all vocab categories from JSON
    categories = load_vocab_categories("data/categories/vocabulary_categories.json")

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

    # Store topic to history
    history.add_category(topic)

    print("\n✅ Post generated:\n")
    print(post["formatted_view"])


if __name__ == "__main__":
    main()
