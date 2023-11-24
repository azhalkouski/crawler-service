import psycopg2
from typing import Optional
from utils.index import openServiceConfig
from services.logger_factory import LoggerFactory


class DataBaseService:
    def __init__(self):
        serviceConfig = openServiceConfig()
        self.db_name = serviceConfig["db_name"]
        self.user_name = serviceConfig["service_user"]
        self.user_pass = serviceConfig["password"]

        loggerFactory = LoggerFactory(__name__)

        self.info_logger = loggerFactory.info_logger
        self.error_logger = loggerFactory.error_logger
        self.critical_logger = loggerFactory.critical_logger


    def get_all_cities(self):
        cities = []
        conn = None

        try:
            conn = psycopg2.connect(f"dbname={self.db_name} \
                                    user={self.user_name} \
                                    password={self.user_pass}")
            print('Database connection open.')
            cur = conn.cursor()

            cur.execute("SELECT * FROM cities;")
            cities = cur.fetchall()

            cur.close()

        except psycopg2.OperationalError as oper_err:
            print('psycopg2::operational error: \n', oper_err)
            self.error_logger.error('psycopg2::operational error: \n', oper_err)

        except psycopg2.ProgrammingError as prog_err:
            print('psycopg2::programming error occured: \n', prog_err)

        except Exception as e:
            print('Something happened at db interaction level: \n', e)
            self.critical_logger.critical('Something happened at db interaction level: \n', e)

        finally:
            if conn is not None:
              conn.close()
              print('\n Database connection closed.')

        return cities


    def save_units_count(self, city_id: int, unit_type: str, count: int) -> None:
        conn = None

        try:
            conn = psycopg2.connect(f"dbname={self.db_name} \
                                    user={self.user_name} \
                                    password={self.user_pass}")
            print('Database connection open.')
            
            cursor = conn.cursor()

            cursor.execute(f"""
                           INSERT INTO total_counts_per_city 
                           (city_id, unit_type, total_count) 
                           VALUES ({city_id}, '{unit_type}', {count});
                           """)

            conn.commit()
            cursor.close()
        except psycopg2.OperationalError as oper_err:
            print('psycopg2::operational error: \n', oper_err)
            self.error_logger.error('psycopg2::operational error: \n', oper_err)

        except psycopg2.ProgrammingError as prog_err:
            print('psycopg2::programming error occured: \n', prog_err)

        except Exception as e:
            print(f'something occured {e}')
            self.critical_logger.critical(f'Something occured {e}')

        finally:
            conn.close()
            print('\n Database connection closed.')
