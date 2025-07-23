# agents/base.py

from abc import ABC, abstractmethod
from pathlib import Path
from pathlib import Path
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, post_type: str, prompt_path: str):
        self.post_type = post_type

        # Always resolve prompt path from project root
        project_root = Path(__file__).resolve().parent.parent  # goes from /agents/generators/base.py to project root
        self.prompt_path = (project_root / prompt_path).resolve()

    def log(self, message: str):
        print(f"[{self.post_type.upper()} Generator] {message}")

    def load_prompt(self) -> str:
        if not self.prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {self.prompt_path}")
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    @abstractmethod
    def run(self, topic: str) -> dict:
        """Generate a post for the given topic."""
        pass
