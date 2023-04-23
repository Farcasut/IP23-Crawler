import psycopg2

from config import  config

def connect():

    """Connect to the PostgreSQL database"""

    conn = None
    try:

        params = config()


        #Connect to the SQL server
        print('Connecting to the database')
        conn = psycopg2.connect(**params)

        #create a cursor
        curr = conn.cursor()

        #For test purpose we will print the version to see if a connection is established
        print('PostgreSQL database version:')
        curr.execute('SELECT version()')


        db_version = curr.fetchone()
        print(db_version)

        #close the communication with PostgreSQL
        curr.close()

    except (Exception, psycopg2.DataError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection is closed')

if __name__ == '__main__':
    connect()