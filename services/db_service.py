import psycopg2
from utils.index import openServiceConfig

conn = None

serviceConfig = openServiceConfig()

db_name = serviceConfig["db_name"]
user_name = serviceConfig["service_user"]
user_pass = serviceConfig["password"]


try:
    conn = psycopg2.connect(f"dbname={db_name} user={user_name} \
                            password={user_pass}")
    cur = conn.cursor()

    cur.execute("SELECT * FROM cities;")
    print(cur.fetchall())

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

