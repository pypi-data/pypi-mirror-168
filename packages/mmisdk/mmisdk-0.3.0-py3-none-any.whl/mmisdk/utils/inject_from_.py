from copy import copy
from typing import Dict, List


def inject_from_(dict: Dict) -> Dict:
    """This method returns a copy of the passed dict, injecting a field "from_", using the same value as field "from". This is needed because 'from' is a reserved keyword in Python."""
    result = copy(dict)
    result["from_"] = result["from"]
    return result


def inject_from_on_all(dict: List[Dict]) -> List[Dict]:
    """"This method returns a copy of the passed list of dicts, injecting a field "from_" on each of them, using the same value as field "from"."""
    return list(map(inject_from_, dict))
