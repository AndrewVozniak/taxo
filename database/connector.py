import psycopg2


def init(host, db, user, password):
    try:
        connection = psycopg2.connect(
            host=host,
            database=db,
            user=user,
            password=password
        )
        cursor = connection.cursor()

        print(f"Connected to database {db} as {user} on {host}")

        return connection, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
