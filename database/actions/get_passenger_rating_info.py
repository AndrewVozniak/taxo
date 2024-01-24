from database.decorators.dict_cursor_decorator import dict_cursor


@dict_cursor
def get_passenger_rating_info_action(cursor, passenger_id):
    cursor.execute(
        'SELECT rating, rating_count FROM passengers WHERE id = %s',
        (passenger_id,)
    )
    return cursor.fetchone()
