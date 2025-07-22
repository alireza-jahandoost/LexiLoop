from agents.generators.vocab_generator import VocabularyPostGenerator

if __name__ == "__main__":
    generator = VocabularyPostGenerator()
    category = input("Category: ")
    post = generator.run(category)

    print("🔤 Vocabulary Post:")
    print(post["formatted_view"])
