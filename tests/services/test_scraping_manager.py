from unittest.mock import MagicMock

import pytest
from crawler_service.services.postgres_service import PostgresService
from crawler_service.services.scraper_service import ScraperService
from crawler_service.services.scraping_manager import ScrapingManager


@pytest.fixture
def mock_invalid_postgres_service():
    """PostgresService which is not an instance of AbstractDBService"""

    class MockPostgresService:
        pass

    return MockPostgresService()


def test_scraping_manager_raises_error_if_db_service_is_invalid(
    mock_invalid_postgres_service
):
    """
    ScrapingManager raises TypeError if db_service is not an instance of
    AbstractDBService
    """
    invalid_postgres_service = mock_invalid_postgres_service
    scraper_service = ScraperService()

    expected_error_message = (
        f"db_service must be an instance of AbstractDBService, "
        f"not {type(invalid_postgres_service)}"
    )

    with pytest.raises(TypeError, match=expected_error_message):
        ScrapingManager(invalid_postgres_service, scraper_service)


def test_scraping_manager_is_initiated_with_passed_args():
    postgres_service = PostgresService()
    scraper_service = ScraperService()

    scraping_manager = ScrapingManager(postgres_service, scraper_service)

    assert scraping_manager.db_service == postgres_service
    assert scraping_manager.scraper_service == scraper_service


def test__handle_city_is_called_once_per_city():
    cities = [(1, "city_1"), (2, "city_2")]
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager.db_service.load_all_cities = lambda: cities
    handle_city_mock = MagicMock()
    scraping_manager._handle_city = handle_city_mock

    scraping_manager.scrape_shallow_all()

    assert handle_city_mock.call_count == len(cities)
    assert handle_city_mock.call_args_list == [
        ((1, "city_1"),),
        ((2, "city_2"),),
    ]


def test__handle_city_is_not_called_if_no_cities():
    cities = []
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager.db_service.load_all_cities = lambda: cities
    handle_city_mock = MagicMock()
    scraping_manager._handle_city = handle_city_mock

    scraping_manager.scrape_shallow_all()

    assert handle_city_mock.call_count == 0
