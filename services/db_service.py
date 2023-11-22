import psycopg2
from utils.index import openServiceConfig


class DataBaseService:
    def __init__(self):
        serviceConfig = openServiceConfig()
        self.db_name = serviceConfig["db_name"]
        self.user_name = serviceConfig["service_user"]
        self.user_pass = serviceConfig["password"]


    def get_all_cities(self):
        cities = []
        conn = None

        try:
            conn = psycopg2.connect(f"dbname={self.db_name} \
                                    user={self.user_name} \
                                    password={self.user_pass}")
            cur = conn.cursor()

            cur.execute("SELECT * FROM cities;")
            cities = cur.fetchall()

            cur.close()

        except psycopg2.OperationalError as oper_err:
            print('psycopg2::operational error: \n', oper_err)
            # TODO: log err to file

        except psycopg2.ProgrammingError as prog_err:
            print('psycopg2::programming error occured: \n', prog_err)
            # TODO: log err to file

        except Exception as e:
            print('Something happened at db interaction level: \n', e)
            # TODO: log err to file

        finally:
            if conn is not None:
              conn.close()
              print('\n Database connection closed.')

        return cities


    def save_units_count(self, cityId, unitType, count):
        """
        - connect
        - cursor
        - INSERT INTO units_count_history (city_id, unit_type, total_count) VALUES (cityId, unitType, count);
        - cursor.commit()
        - cursor.close
        - connection.close
        - return cities_list
        """
        pass