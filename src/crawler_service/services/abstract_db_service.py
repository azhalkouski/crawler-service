import abc

"""DB service interface"""


class AbstractDBService(abc.ABC):
    @abc.abstractmethod
    def load_all_cities(self):
        """Load all cities from DB"""

    @abc.abstractmethod
    def save_units_count(
        self, city_id: int, unit_type: str, transaction_type: str, count: int
    ):
        """Save units count to DB"""
