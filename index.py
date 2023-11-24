import logging
from services.scraper_service import ScraperService
from services.db_service import DataBaseService


def process_cities(cities):
    logging.info('Scraping process is running.')
    BREAKPOINT_COUNT = len(cities) + 5
    iteration_count = 0

    while len(cities) > 0:
        iteration_count += 1
        city = cities.pop(0)
        city_id, city_name = city

        try:
            count_of_units = scraperService\
              .scrape_appartments_count_for_city(city_name)
        except Exception as e:
            cities.append(city)

            error_log = f"Failed to scrape for {city_name} with an error: {e}"
            print(error_log)
            logging.error(error_log)
        
            if iteration_count > BREAKPOINT_COUNT:
                critical_log = (f"BREAKING THE CYCLE because of constantly "
                      f"failing to scrape for {cities} with an error: {e}")
                print(critical_log)
                logging.critical(critical_log)

                break
        else:
            print(city_id, city_name, count_of_units)
            dataBaseService.save_units_count(city[0], 'apartment',
                                             count_of_units)
    else:
        logging.info('Scraping process completed successfully.')


if __name__ == '__main__':
    log_format = '%(levelname)s:%(name)s:%(asctime)s:%(message)s'
    logging.basicConfig(filename='info_level_logs.log', encoding='utf-8',
                        level=logging.INFO, format=log_format)
    logging.info('Scraping process is being started.')
    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    process_cities(cities)