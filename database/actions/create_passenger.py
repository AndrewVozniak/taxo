def create_passenger_action(cursor, user_id, name):
    passenger = (user_id, name)

    try:
        cursor.execute("INSERT INTO passengers VALUES (%s, %s)", passenger)
        cursor.connection.commit()

        return {
            "id": user_id,
            "name": name,
        }

    except Exception as e:
        print(e)
        return None
