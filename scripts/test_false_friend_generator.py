from agents.generators.false_friend_generator import FalseFriendPostGenerator

if __name__ == "__main__":
    generator = FalseFriendPostGenerator()
    category = input("False Friend (Italian word): ")
    post = generator.run(category)

    print("\n🚫 False Friend Post:")
    print(post["formatted_view"])
