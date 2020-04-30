import psycopg2

try:
    connection = psycopg2.connect(
        user='postgres',
        password='postgrest',
        host='192.168.86.108',
        port='32834',
        #database='postgres_db'
    )

    cursor = connection.cursor()
    print ( connection.get_dsn_parameters(),"\n")

    results = cursor.execute(
                    """CREATE TABLE IF NOT EXISTS 
                            site_pages (
                                id           BIGSERIAL PRIMARY KEY, 
                                number       INTEGER NOT NULL,
                                site_id      INTEGER NOT NULL UNIQUE,
                                last_date    TIMESTAMP,
                                last_user    VARCHAR(100),
                                create_date  TIMESTAMP,
                                create_user  VARCHAR(100)
                        )"""
    )

    results = cursor.execute("""SELECT * FROM site_pages""")
    print(results)

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")