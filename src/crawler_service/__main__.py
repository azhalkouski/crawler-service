import time

from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.services.postgres_service import PostgresService
from crawler_service.services.scraper_service import ScraperService
from crawler_service.services.scraping_manager import ScrapingManager

if __name__ == "__main__":
    loggerFactory = LoggerFactory("root")
    info_logger = loggerFactory.info_logger

    info_logger.info("Scraping process is being started.")

    # Dependency Injection
    postgres_service = PostgresService()
    scraper_service = ScraperService()
    scraping_manager = ScrapingManager(postgres_service, scraper_service)

    while True:
        scraping_manager.scrape_shallow_all()
        print("Scraping session completed.")
        time.sleep(3600)  # 1h
