from typing import Dict


def replace(string: str, dictionary: Dict[str, str]) -> str:
    if not isinstance(string, str):
        raise TypeError("accept string type")

    trans = str.maketrans(dictionary)
    return string.translate(trans)
