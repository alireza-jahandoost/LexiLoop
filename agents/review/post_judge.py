import json
from langchain.schema import HumanMessage
from langchain_utils.model_config import get_llm_model
from agents.base import BaseAgent


class PostJudgeAgent(BaseAgent):
    def __init__(self, temperature: float = 0.3):
        super().__init__(post_type="post", prompt_path="data/prompts/evaluate_generated_text_post.txt")
        self.llm = get_llm_model(temperature=temperature)

    def judge(self, post: dict) -> dict:
        """
        Input: a post dict with keys: type, topic, content
        Output: dict with keys: verdict and reason
        """
        try:
            prompt_template = self.load_prompt()
        except FileNotFoundError as e:
            return {"verdict": "reject", "reason": str(e)}

        # Insert post content into the prompt template
        filled_prompt = prompt_template.replace("[POST]", post["formatted_view"])

        # Call the LLM
        response = self.llm.invoke([HumanMessage(content=filled_prompt)])

        # Parse and return the JSON result
        return self._parse_json(response.content)

    def _parse_json(self, raw: str) -> dict:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "verdict": "reject",
                "reason": "Invalid JSON format returned by LLM"
            }

    # Optional: implement abstract method if needed
    def run(self, topic: str) -> dict:
        """Not used for judging; required by BaseAgent"""
        raise NotImplementedError("Use the 'judge' method for evaluating posts.")
