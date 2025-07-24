from agents.generators.grammar_generator import GrammarPostGenerator

if __name__ == "__main__":
    generator = GrammarPostGenerator()
    category = input("Category: ")
    post = generator.run(category)

    print("🔤 Grammar Post:")
    print(post["formatted_view"])