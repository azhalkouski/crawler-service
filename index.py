from services.scraper_service import ScraperService
from services.db_service import DataBaseService


dataBaseService = DataBaseService()
scraperService = ScraperService()

cities = dataBaseService.get_all_cities()

for city in cities:
    count = scraperService.scrape_appartments_count_for_city(city[1])
    print(city[0], city[1], count)
