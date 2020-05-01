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
    results = ''

    print(results)
    #results = cursor.execute("""SELECT * FROM site_pages""")

    print(type(results))

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