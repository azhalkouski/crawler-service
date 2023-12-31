from threading import Thread
from typing import TypeVar

from crawler_service.services.abstract_db_service import AbstractDBService
from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.services.scraper_service import ScraperService

AbstractDBServiceT = TypeVar("AbstractDBServiceT", bound=AbstractDBService)
ScraperServiceT = TypeVar("ScraperServiceT", bound=ScraperService)


class ScrapingManager:
    """
    ScrapingManager is responsible for:
    - obtaining required data from DB
    - scraping data from the web (invoking ScraperService)
    - saving obtained data to DB
    """

    def __init__(
        self, db_service: AbstractDBServiceT, scraper_service: ScraperServiceT
    ):
        # Inversion of Control
        if not isinstance(db_service, AbstractDBService):
            raise TypeError(
                f"db_service must be an instance of AbstractDBService, "
                f"not {type(db_service)}"
            )
        self.db_service = db_service
        self.scraper_service = scraper_service

        loggerFactory = LoggerFactory(__name__)

        self.info_logger = loggerFactory.info_logger
        self.error_logger = loggerFactory.error_logger
        self.critical_logger = loggerFactory.critical_logger

    def scrape_shallow_all(self):
        self.info_logger.info("Scraping process is being started.")

        cities = self.db_service.load_all_cities()

        if len(cities) == 0:
            return None

        for city in cities:
            self._handle_city(*city)

    def _handle_city(self, city_id, city_name):
        """
        Processing for each city is spread across three separate threads.
        Notes to remember: `join` method blocks the calling thread until it completes
        its execution
        """
        print(f"{city_id}-{city_name}")

        apartments_thread = Thread(
            target=self._process_apartments, args=[city_id, city_name]
        )
        houses_thread = Thread(target=self._process_houses, args=[city_id, city_name])
        rooms_thread = Thread(target=self._process_rooms, args=[city_id, city_name])

        apartments_thread.start()
        houses_thread.start()
        rooms_thread.start()

        apartments_thread.join()
        houses_thread.join()
        rooms_thread.join()

    def _process_apartments(self, city_id, city_name):
        self._scrape_for_unit(city_id, city_name, "apartment", "sell")
        self._scrape_for_unit(city_id, city_name, "apartment", "rent")

    def _process_houses(self, city_id, city_name):
        self._scrape_for_unit(city_id, city_name, "house", "sell")
        self._scrape_for_unit(city_id, city_name, "house", "rent")

    def _process_rooms(self, city_id, city_name):
        self._scrape_for_unit(city_id, city_name, "room", "rent")

    def _scrape_for_unit(self, city_id, city_name, type_of_unit, type_of_deal):
        """
        Might not go well with the first attempt.
        Give 3 attempts.
        Log critical if an attempt fails.
        """
        print(f"{city_id}-{city_name}-{type_of_unit}-{type_of_deal}-running")

        ATTEMPTS_COUNT = 3

        for _ in range(ATTEMPTS_COUNT):
            try:
                count_of_units = self.scraper_service.scrape(
                    city_name, type_of_unit, type_of_deal
                )
            except Exception as e:
                critical_log = (
                    f"Scraping has failed city={city_name}, "
                    f"type_of_unit={type_of_unit}, "
                    f"type_of_deal={type_of_deal}"
                    "check the screenshots for more details"
                    f"Error: {str(e)}"
                )
                print(critical_log)
                self.critical_logger.critical(critical_log)
            else:
                print(
                    f"{city_id}-{city_name}-{type_of_unit}-"
                    f"{type_of_deal}-{count_of_units}"
                )
                self.db_service.save_units_count(
                    city_id, type_of_unit, type_of_deal, count_of_units
                )
                break
