import time

from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.services.postgres_service import PostgresService
from crawler_service.services.scraper_service import ScraperService

if __name__ == "__main__":
    loggerFactory = LoggerFactory("root")
    info_logger = loggerFactory.info_logger

    info_logger.info("Scraping process is being started.")

    postgres_service = PostgresService()
    # Dependency Injection
    scraperService = ScraperService(postgres_service)

    while True:
        scraperService.process_cities()
        time.sleep(3600)  # 1h
