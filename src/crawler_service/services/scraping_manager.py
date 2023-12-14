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

        BREAKPOINT_COUNT = len(cities) + 5
        iteration_count = 0

        while len(cities) > 0:
            iteration_count += 1
            city = cities.pop(0)
            city_id, city_name = city

            try:
                count_of_units = self.scraper_service.scrape_apartments_count_for_city(
                    city_name
                )
            except Exception as e:
                cities.append(city)

                error_log = f"Failed to scrape for {city_name} with an error: {e}"
                print(error_log)
                self.error_logger.error(error_log)

                if iteration_count > BREAKPOINT_COUNT:
                    critical_log = (
                        f"BREAKING THE CYCLE because of constantly "
                        f"failing to scrape for {cities} with an error: {e}"
                    )
                    print(critical_log)
                    self.critical_logger.critical(critical_log)

                    break
            else:
                print(city_id, city_name, count_of_units)
                self.db_service.save_units_count(city[0], "apartment", count_of_units)
        else:
            print("Scraping process completed successfully.")
            self.info_logger.info("Scraping process completed successfully.")
