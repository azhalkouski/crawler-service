import json
import re


def openServiceConfig():
    serviceConfig = None

    try:
        with open("src/searchConfig.json") as search_config_file:
            serviceConfig = json.load(search_config_file)

    except Exception as e:
        print(f"Exception while reading serviceConfig: {e}")
        # TODO: log the error to file

    return serviceConfig


def extract_numeric_word(str):
    """
    Extracts a numeric value out of a string if the numeric value exists as
    a standalone word. The value is of type int. Uses a regular expression.
    """
    whole_numeric_word_pattern = r"\b\d+\b"
    numeric_matches = re.findall(whole_numeric_word_pattern, str)
    if numeric_matches:
        return int(numeric_matches[0])
    else:
        # TODO: log the str so that the unknown or error case can be handled
        # if there's no numeric word, either the scraping hasn't worked out,
        # or the target website has introduced a breaking change to its UI
        return None
