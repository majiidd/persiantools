import re
from typing import Dict


def replace(string: str, dictionary: Dict[str, str]) -> str:
    if not isinstance(string, str):
        raise TypeError("accept string type")

    pattern = re.compile("|".join(dictionary.keys()))
    return pattern.sub(lambda x: dictionary[x.group()], string)
