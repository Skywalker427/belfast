from typing import Dict


def filter_none(d: Dict) -> Dict:
    """
    Filter out keys with None values from a dictionary

    Args:
        d (Dict): Dictionary to filter

    Returns:
        Dict: Filtered dictionary
    """
    return {k: v for k, v in d.items() if v is not None}