from typing import Dict, Any


def match_criteria(item: Dict[str, Any], criterion: Dict[str, Any]) -> bool:
    return all(item.get(key) == value for key, value in criterion.items())
