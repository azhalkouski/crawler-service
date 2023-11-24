import logging
from services.scraper_service import ScraperService
from services.db_service import DataBaseService


if __name__ == '__main__':
    log_format = '%(levelname)s:%(name)s:%(asctime)s:%(message)s'
    logging.basicConfig(filename='info_level_logs.log', encoding='utf-8',
                        level=logging.INFO, format=log_format)
    logging.info('Scraping process is being started.')

    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    scraperService.process_cities(cities)
