from pathlib import Path
import json

def load_categories(path: str) -> list[str]:
    full_path = Path(__file__).resolve().parent.parent / path
    if not full_path.exists():
        raise f"❌ Category file not found: {full_path}"

    with open(full_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return [entry["category"] for entry in data if "category" in entry]
        except json.JSONDecodeError:
            raise f"❌ Failed to parse JSON file: {full_path}"
