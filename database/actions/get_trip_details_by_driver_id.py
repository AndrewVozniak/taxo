from database.decorators.dict_cursor_decorator import dict_cursor


@dict_cursor
def get_trip_details_by_driver_id_action(cursor, user_id):
    cursor.execute("""
        SELECT * FROM trips where driver_id = %s ORDER BY id DESC LIMIT 1
    """, (user_id,))

    return cursor.fetchone()
