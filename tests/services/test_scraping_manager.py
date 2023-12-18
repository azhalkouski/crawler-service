from unittest.mock import MagicMock, call, patch

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


def test__handle_city_starts_processing_apartments_houses_and_rooms_for_city():
    city_id = 1
    city_name = "city_1"
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager._process_apartments = MagicMock()
    scraping_manager._process_houses = MagicMock()
    scraping_manager._process_rooms = MagicMock()

    scraping_manager._handle_city(city_id, city_name)

    scraping_manager._process_apartments.assert_called_once_with(city_id, city_name)
    scraping_manager._process_houses.assert_called_once_with(city_id, city_name)
    scraping_manager._process_rooms.assert_called_once_with(city_id, city_name)


def test__handle_city_starts_threads_and_waits_for_completion():
    city_id = 1
    city_name = "city_1"
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager._process_apartments = MagicMock()
    scraping_manager._process_houses = MagicMock()
    scraping_manager._process_rooms = MagicMock()

    with patch("crawler_service.services.scraping_manager.Thread") as mock_thread:
        apartments_thread = MagicMock()
        houses_thread = MagicMock()
        rooms_thread = MagicMock()
        mock_thread.side_effect = [apartments_thread, houses_thread, rooms_thread]

        scraping_manager._handle_city(city_id, city_name)

        apartments_thread.start.assert_called_once()
        houses_thread.start.assert_called_once()
        rooms_thread.start.assert_called_once()

        apartments_thread.join.assert_called_once()
        houses_thread.join.assert_called_once()
        rooms_thread.join.assert_called_once()


def test_all_possible_deals_are_processed():
    city_id = 1
    city_name = "city_1"
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager.scraper_service.scrape = MagicMock()
    scraping_manager.db_service.save_units_count = MagicMock()

    scraping_manager._handle_city(city_id, city_name)

    assert scraping_manager.scraper_service.scrape.call_count == 5
    assert (
        call(city_name, "apartment", "sell")
        in scraping_manager.scraper_service.scrape.call_args_list
    )
    assert (
        call(city_name, "apartment", "rent")
        in scraping_manager.scraper_service.scrape.call_args_list
    )
    assert (
        call(city_name, "house", "sell")
        in scraping_manager.scraper_service.scrape.call_args_list
    )
    assert (
        call(city_name, "house", "rent")
        in scraping_manager.scraper_service.scrape.call_args_list
    )
    assert (
        call(city_name, "room", "rent")
        in scraping_manager.scraper_service.scrape.call_args_list
    )


def test_scraped_data_is_saved_if_no_exception_raised():
    city_id = 1
    city_name = "city_1"
    mock_units_count = 5
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager.scraper_service.scrape = MagicMock()
    scraping_manager.db_service.save_units_count = MagicMock()
    scraping_manager.scraper_service.scrape.return_value = mock_units_count

    scraping_manager._handle_city(city_id, city_name)

    assert scraping_manager.db_service.save_units_count.call_count == 5

    assert (
        call(city_id, "apartment", "sell", mock_units_count)
        in scraping_manager.db_service.save_units_count.call_args_list
    )
    assert (
        call(city_id, "apartment", "rent", mock_units_count)
        in scraping_manager.db_service.save_units_count.call_args_list
    )
    assert (
        call(city_id, "house", "sell", mock_units_count)
        in scraping_manager.db_service.save_units_count.call_args_list
    )
    assert (
        call(city_id, "house", "rent", mock_units_count)
        in scraping_manager.db_service.save_units_count.call_args_list
    )
    assert (
        call(city_id, "room", "rent", mock_units_count)
        in scraping_manager.db_service.save_units_count.call_args_list
    )


def test_scraped_data_is_saved_and_critical_error_is_logged_if_no_exception_raised():
    city_id = 1
    city_name = "city_1"
    # since each scrape has 3 attempts, we expect 15 critical logs
    expected_critical_logs = 15
    scraping_manager = ScrapingManager(PostgresService(), ScraperService())
    scraping_manager.critical_logger.critical = MagicMock()
    scraping_manager.scraper_service.scrape = MagicMock()
    scraping_manager.db_service.save_units_count = MagicMock()

    exception_message = "Exception raised"
    scraping_manager.scraper_service.scrape.side_effect = Exception(exception_message)

    scraping_manager._handle_city(city_id, city_name)

    assert scraping_manager.db_service.save_units_count.call_count == 0
    assert (
        scraping_manager.critical_logger.critical.call_count == expected_critical_logs
    )

    # make sure the logs have expected structure
    apartment_rent_log = (
        f"Scraping has failed city={city_name}, "
        f"type_of_unit=apartment, "
        f"type_of_deal=rent"
        "check the screenshots for more details"
        f"Error: {exception_message}"
    )
    assert (
        call(apartment_rent_log)
        in scraping_manager.critical_logger.critical.call_args_list
    )
