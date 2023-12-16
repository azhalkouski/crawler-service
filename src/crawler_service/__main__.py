import time

from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.services.postgres_service import PostgresService
from crawler_service.services.scraper_service import ScraperService
from crawler_service.services.scraping_manager import ScrapingManager


def create_scraping_manager() -> ScrapingManager:
    # Dependency Injection
    postgres_service = PostgresService()
    scraper_service = ScraperService()

    return ScrapingManager(postgres_service, scraper_service)


if __name__ == "__main__":
    loggerFactory = LoggerFactory("root")
    info_logger = loggerFactory.info_logger

    info_logger.info("Scraping process is being started.")

    scraping_manager = create_scraping_manager()

    while True:
        scraping_manager.scrape_shallow_all()
        print("Scraping session completed.")
        time.sleep(3600)  # 1h
