import json
import re
from datetime import datetime

from crawler_service.services.logger_factory import LoggerFactory


def open_service_config(path_to_file="search_config.json"):
    serviceConfig = None
    loggerFactory = LoggerFactory(__name__)
    error_logger = loggerFactory.error_logger

    try:
        with open(path_to_file) as search_config_file:
            serviceConfig = json.load(search_config_file)

    except FileNotFoundError as e:
        print(
            f"FileNotFoundError while reading serviceConfig at path {path_to_file}: {e}"
        )
        error_logger.error(
            f"FileNotFoundError while reading serviceConfig at path {path_to_file}: {e}"
        )

    except Exception as e:
        print(f"Exception while reading serviceConfig: {e}")
        error_logger.error(f"Exception while reading serviceConfig: {e}")

    return serviceConfig


def extract_numeric_word(str):
    """
    Extracts a numeric value out of a string if the numeric value exists as
    a standalone word. The value is of type int. Uses a regular expression.
    """
    loggerFactory = LoggerFactory(__name__)
    critical_logger = loggerFactory.critical_logger

    whole_numeric_word_pattern = r"\b\d+\b"
    numeric_matches = re.findall(whole_numeric_word_pattern, str)
    if numeric_matches:
        return int(numeric_matches[0])
    else:
        critical_logger.critical(
            f"The input srting scrapped form the target web site could have been \
              changed. Could not extract numeric value from string {str}"
        )
        return None


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
