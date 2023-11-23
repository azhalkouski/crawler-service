from services.scraper_service import ScraperService
from services.db_service import DataBaseService


def process_cities(cities):
    BREAKPOINT_COUNT = len(cities) + 5
    iteration_count = 0

    while len(cities) > 0:
        iteration_count += 1
        city = cities.pop(0)
        city_id, city_name = city

        try:
            count_of_units = scraperService.scrape_appartments_count_for_city(city_name)
            print(city_id, city_name, count_of_units)
            dataBaseService.save_units_count(city[0], 'apartment', count_of_units)

        except Exception as e:
            cities.append(city)
            print(f"Failed to scrape for {city_name} with an error: {e}")
        
            if iteration_count > BREAKPOINT_COUNT:
                print(f"BREAKING THE CYCLE because of constantly failing to "
                      f"scrape for {cities} with an error: {e}")
                break


if __name__ == '__main__':
    dataBaseService = DataBaseService()
    scraperService = ScraperService()

    cities = dataBaseService.get_all_cities()

    process_cities(cities)