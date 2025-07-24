# agents/generators/grammar_generator.py

from agents.generators.base_generator import BaseGenerator


class GrammarPostGenerator(BaseGenerator):
    def __init__(self, prompt_path="data/prompts/generate_grammar_post.txt"):
        super().__init__(post_type="grammar", prompt_path=prompt_path)

    def format_view(self, parsed: dict) -> str:
        lines = []

        # Title
        lines.append(f"📚 Grammar Tip: *{parsed['category']}*\n")

        # Tip
        lines.append(f"💡 Tip:\n{parsed['tip']}\n")

        # Examples
        lines.append("📝 Examples:")
        for ex in parsed.get("examples", []):
            lines.append(f"🇮🇹 {ex['italian']}")
            lines.append(f"🇺🇸 {ex['english']}\n")

        # Optional note
        if parsed.get("note"):
            lines.append(f"🧠 Note:\n{parsed['note']}")

        return "\n".join(lines).strip()
