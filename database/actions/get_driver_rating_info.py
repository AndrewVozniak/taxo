from database.decorators.dict_cursor_decorator import dict_cursor


@dict_cursor
def get_driver_rating_info_action(cursor, driver_id):
    cursor.execute(
        'SELECT rating, rating_count FROM drivers WHERE id = %s',
        (driver_id,)
    )
    return cursor.fetchone()
