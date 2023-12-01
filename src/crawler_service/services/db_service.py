from context_managers.db_connection import DBConnection
from utils.index import openServiceConfig


class DataBaseService:
    def __init__(self):
        serviceConfig = openServiceConfig()
        self.db_name = serviceConfig["db_name"]
        self.user_name = serviceConfig["service_user"]
        self.user_pass = serviceConfig["password"]

    def get_all_cities(self):
        cities = []

        with DBConnection(self.db_name, self.user_name, self.user_pass) as (_, cur):
            if cur is None:
                return []

            cur.execute("SELECT * FROM cities;")
            cities = cur.fetchall()

        return cities

    def save_units_count(self, city_id: int, unit_type: str, count: int) -> None:
        with DBConnection(self.db_name, self.user_name, self.user_pass) as (conn, cur):
            if cur is None:
                return None

            cur.execute(
                f"""
                          INSERT INTO total_counts_per_city
                          (city_id, unit_type, total_count)
                          VALUES ({city_id}, '{unit_type}', {count});
                          """
            )

            conn.commit()
