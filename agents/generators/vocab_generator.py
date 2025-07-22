import json
from langchain_utils.model_config import get_llm_model
from langchain.schema import HumanMessage
from agents.generators.base import BasePostGenerator


class VocabularyPostGenerator(BasePostGenerator):
    def __init__(self, prompt_path="data/prompts/generate_vocabulary_post.txt"):
        super().__init__(post_type="vocab_json", prompt_path=prompt_path)
        self.llm = get_llm_model(temperature=1)

    def run(self, category: str) -> dict:
        self.log(f"Generating JSON vocabulary post for category: {category}")
        prompt = self.load_prompt().replace("[CATEGORY]", category)
        response = self.llm.invoke([HumanMessage(content=prompt)])

        try:
            parsed = json.loads(response.content.strip())
        except json.JSONDecodeError as e:
            self.log(f"Failed to parse JSON: {e}")
            raise ValueError("Model did not return valid JSON")

        # Convert JSON back to display format
        formatted_lines = [f"{parsed['topic']}"]
        for item in parsed["vocabulary"]:
            formatted_lines.append(
                f"\n{item['emoji']} **{item['word_it']}** — {item['meaning_en']}\n"
                f"🗣️ {item['example_it']}\n"
                f"💬 ({item['example_en']})"
            )
        formatted_view = "\n".join(formatted_lines)

        return {
            "type": self.post_type,
            "topic": category,
            "content": parsed,
            "formatted_view": formatted_view.strip(),
            "media": None
        }
