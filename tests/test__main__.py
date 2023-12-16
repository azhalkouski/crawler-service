from crawler_service.__main__ import create_scraping_manager
from crawler_service.services.postgres_service import PostgresService
from crawler_service.services.scraping_manager import ScrapingManager


def test_scraping_manager_is_created_with_postgres_service():
    scraping_manager = create_scraping_manager()

    assert isinstance(scraping_manager, ScrapingManager)
    assert isinstance(scraping_manager.db_service, PostgresService)
