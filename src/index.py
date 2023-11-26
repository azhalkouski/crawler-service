import logging
from services.scraper_service import ScraperService
from services.db_service import DataBaseService
from services.logger_factory import LoggerFactory


if __name__ == '__main__':
    loggerFactory = LoggerFactory('root')
    info_logger = loggerFactory.info_logger

    info_logger.info('Scraping process is being started.')

    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    scraperService.process_cities(cities)
