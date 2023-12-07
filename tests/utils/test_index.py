import json

from crawler_service.utils.index import open_service_config


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
