import time
from datetime import datetime

from crawler_service.services.db_service import DataBaseService
from crawler_service.services.logger_factory import LoggerFactory
from crawler_service.services.scraper_service import ScraperService

if __name__ == "__main__":
    loggerFactory = LoggerFactory("root")
    info_logger = loggerFactory.info_logger

    info_logger.info("Scraping process is being started.")

    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    while True:
        print(f'processing at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        scraperService.process_cities(cities)
        time.sleep(3600)  # 1h
