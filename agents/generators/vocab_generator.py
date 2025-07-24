# agents/generators/vocabulary_generator.py

from agents.generators.base_generator import BaseGenerator


class VocabularyPostGenerator(BaseGenerator):
    def __init__(self, prompt_path="data/prompts/generate_vocabulary_post.txt"):
        super().__init__(post_type="vocab", prompt_path=prompt_path)

    def format_view(self, parsed: dict) -> str:
        lines = [f"**{parsed['topic']}**"]
        for item in parsed["vocabulary"]:
            lines.append(
                f"\n{item['emoji']} **{item['word_it']}** — {item['meaning_en']}\n"
                f"🗣️ {item['example_it']}\n"
                f"💬 ({item['example_en']})"
            )
        return "\n".join(lines)