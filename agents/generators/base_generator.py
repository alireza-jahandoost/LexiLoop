# agents/generators/base_generator.py

import json
from langchain_utils.model_config import get_llm_model
from langchain.schema import HumanMessage
from agents.base import BaseAgent


class BaseGenerator(BaseAgent):
    def __init__(self, post_type: str, prompt_path: str):
        super().__init__(post_type=post_type, prompt_path=prompt_path)
        self.llm = get_llm_model(temperature=1)

    def generate_json(self, topic: str) -> dict:
        self.log(f"Generating JSON post for topic: {topic}")
        prompt = self.load_prompt().replace("[CATEGORY]", topic)
        response = self.llm.invoke([HumanMessage(content=prompt)])

        try:
            parsed = json.loads(response.content.strip())
        except json.JSONDecodeError as e:
            self.log(f"Failed to parse JSON: {e}")
            raise ValueError("Model did not return valid JSON")

        return parsed

    def run(self, topic: str) -> dict:
        parsed = self.generate_json(topic)
        formatted_view = self.format_view(parsed)
        return {
            "type": self.post_type,
            "topic": topic,
            "content": parsed,
            "formatted_view": formatted_view.strip(),
            "media": None
        }

    def format_view(self, parsed: dict) -> str:
        """Override in subclass to customize post formatting."""
        raise NotImplementedError("Subclasses must implement format_view()")
