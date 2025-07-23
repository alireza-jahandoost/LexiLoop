import json
from pathlib import Path
from typing import Dict
from datetime import datetime

from helper_functions.merge_dicts import merge_dicts


def log_dict_to_file(
    output_path: str,
    *dicts: Dict,
    ensure_ascii: bool = False
) -> None:
    """
    Merges multiple dictionaries, adds a UTC timestamp if missing,
    and appends the result as a JSON line to the specified file.

    Args:
        output_path: Path to the log file (will be created if it doesn't exist)
        *dicts: Any number of flat dictionaries to merge and log
        ensure_ascii: If True, escape non-ASCII characters in the output
    """
    merged = merge_dicts(*dicts)

    # Add timestamp if not already present
    merged.setdefault("timestamp", datetime.utcnow().isoformat())

    log_path = Path(output_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(merged, ensure_ascii=ensure_ascii) + "\n")
