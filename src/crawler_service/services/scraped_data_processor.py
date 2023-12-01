from crawler_service.services.db_service import DataBaseService


class ScrapedDataProcessor:
    """
    A man in the middle's purpose is to split concerns of scraping and
    communicatin with the database. The ScraperService obtains data and just
    hands it over.
    The man in the middle, ScrapedDataProcessor, accepts the data, decides
    whether it should be saved (or which piecies of data should be saved),
    and hands the chosen data to the DataBaseService, which in turn
    communicates with the database.
    """

    def __init__(self):
        self.dataBaseService = DataBaseService()

    def process_aggregates_by_city(
        self, city_id: int, unit_type: str, count: int
    ) -> None:
        self.dataBaseService.save_units_count(city_id, unit_type, count)
