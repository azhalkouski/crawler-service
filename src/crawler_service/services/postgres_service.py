from crawler_service.context_managers.postgres_connection import PostgresConnection
from crawler_service.services.abstract_db_service import AbstractDBService
from crawler_service.utils.index import open_service_config


class PostgresService(AbstractDBService):
    def __init__(self):
        serviceConfig = open_service_config()
        self.db_name = serviceConfig["db_name"]
        self.user_name = serviceConfig["username"]
        self.user_pass = serviceConfig["password"]

    def load_all_cities(self):
        cities = []

        with PostgresConnection(self.db_name, self.user_name, self.user_pass) as (
            _,
            cur,
        ):
            if cur is None:
                return []

            cur.execute("SELECT * FROM cities;")
            cities = cur.fetchall()

        return cities

    def save_units_count(
        self, city_id: int, unit_type: str, transaction_type: str, count: int
    ) -> None:
        with PostgresConnection(self.db_name, self.user_name, self.user_pass) as (
            conn,
            cur,
        ):
            if cur is None:
                return None

            cur.execute(
                f"""INSERT INTO total_counts_per_city\
                  (city_id, unit_type, transaction_type, total_count) VALUES\
                    ({city_id}, '{unit_type}', '{transaction_type}',\
                      {count});"""
            )

            conn.commit()
