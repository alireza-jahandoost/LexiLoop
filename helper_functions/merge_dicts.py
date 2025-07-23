from typing import Dict


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merges multiple dictionaries into one flat dictionary.

    Args:
        *dicts: Any number of dictionaries

    Returns:
        A single merged dictionary. If duplicate keys exist, later ones override earlier ones.
    """
    merged = {}
    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")
        merged.update(d)
    return merged
