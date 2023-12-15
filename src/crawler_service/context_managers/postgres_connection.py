import psycopg2
from crawler_service.services.logger_factory import LoggerFactory


# rename to PostgresConnection
class PostgresConnection:
    """Context manager for managing connection to the database"""

    def __init__(self, db_name, user_name, user_pass):
        self.db_name = db_name
        self.user_name = user_name
        self.user_pass = user_pass

        self.conn = None
        self.cursor = None

        loggerFactory = LoggerFactory(__name__)

        self.info_logger = loggerFactory.info_logger
        self.error_logger = loggerFactory.error_logger
        self.critical_logger = loggerFactory.critical_logger

    def __enter__(self):
        """init connection to database and return connection object"""

        try:
            self.conn = psycopg2.connect(
                f"dbname={self.db_name} \
                                    user={self.user_name} \
                                    password={self.user_pass}"
            )
            self.cursor = self.conn.cursor()

        except psycopg2.OperationalError as oper_err:
            print("psycopg2::operational error: \n", oper_err)
            self.error_logger.error(f"psycopg2::operational error: {oper_err}")

        except psycopg2.ProgrammingError as prog_err:
            print(f"psycopg2::programming error occured: {prog_err}")

        except Exception as e:
            print("Something happened at db interaction level: \n", e)
            self.critical_logger.critical(
                f"Something happened at db interaction level: {e}"
            )
        else:
            return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """close connection"""
        if exc_type is not None:
            print("exc_type, exc_value, traceback")
            self.error_logger.error(f"{exc_type} | {exc_value} | {traceback}")

        if self.conn is not None:
            self.cursor.close()
            self.conn.close()
