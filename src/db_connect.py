import psycopg2
from db_config import config

def testConnect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = connect()
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        close(conn)

def connect():
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        return psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close(conn):
    if conn is not None:
        conn.close()
        print('Database connection closed.')