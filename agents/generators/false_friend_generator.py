from agents.generators.base_generator import BaseGenerator


class FalseFriendPostGenerator(BaseGenerator):
    def __init__(self, prompt_path="data/prompts/generate_false_friend_post.txt"):
        super().__init__(post_type="false_friend", prompt_path=prompt_path)

    def format_view(self, parsed: dict) -> str:
        lines = []

        # Title
        lines.append(f"🚫 False Friend: *{parsed['italian']}*\n")

        # Looks like and true meaning
        lines.append(f"❌ Looks like: *{parsed['looks_like']}*")
        lines.append(f"✅ Actually means: *{parsed['true_meaning']}*\n")

        # Example sentence
        if "example" in parsed:
            lines.append("📝 Example:")
            lines.append(f"🇮🇹 {parsed['example']['italian']}")
            lines.append(f"🇺🇸 {parsed['example']['english']}\n")

        # Optional note
        if parsed.get("note"):
            lines.append(f"🧠 Note: {parsed['note']}")

        return "\n".join(lines).strip()
