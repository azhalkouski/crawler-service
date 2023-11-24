import logging
from services.scraper_service import ScraperService
from services.db_service import DataBaseService
from services.logger_factory import LOG_FORMAT


if __name__ == '__main__':
    logging.basicConfig(filename='info_level_logs.log', encoding='utf-8',
                        level=logging.INFO, format=LOG_FORMAT)
    logging.info('Scraping process is being started.')

    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    scraperService.process_cities(cities)
