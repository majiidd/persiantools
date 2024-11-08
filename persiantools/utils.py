import re


def replace(string: str, dictionary: dict[str, str]) -> str:
    """
    Replace occurrences of keys in the dictionary with their corresponding values in the given string.

    Args:
    string (str): The string to perform replacements on.
    dictionary (Dict[str, str]): A dictionary where the keys are the substrings to be replaced and the values are the replacements.

    Returns:
    str: The modified string with replacements made.

    Raises:
    TypeError: If the input string is not of type str.
    """
    if not isinstance(string, str):
        raise TypeError("Input must be of type str")

    if not dictionary:
        return string

    pattern = re.compile("|".join(re.escape(key) for key in dictionary))
    return pattern.sub(lambda x: dictionary[x.group()], string)
