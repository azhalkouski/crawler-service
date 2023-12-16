import json
from datetime import datetime

from crawler_service.utils.index import (
    extract_numeric_word,
    get_current_time,
    open_service_config,
)


def test_open_service_config_when_file_exists():
    with open("tests/test_data/service_config.json") as f:
        expected = json.load(f)

    serviceConfig = open_service_config("tests/test_data/service_config.json")

    assert serviceConfig is not None
    assert serviceConfig["targetServiceUrl"] == expected["targetServiceUrl"]
    assert serviceConfig["acceptCookiesBtnId"] == serviceConfig["acceptCookiesBtnId"]


def test_openServiceConfig_when_file_missing():
    serviceConfig = open_service_config("tests/test_data/missing_config.json")

    assert serviceConfig is None


def test_extract_numeric_word_when_numeric_value_exists():
    string = "The price is $100"
    result = extract_numeric_word(string)
    assert result == 100


def test_extract_numeric_word_when_numeric_value_does_not_exist():
    string = "No numeric value in this string"
    result = extract_numeric_word(string)
    assert result is None


def test_get_current_time():
    current_time = get_current_time()
    assert isinstance(current_time, str)
    assert datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
