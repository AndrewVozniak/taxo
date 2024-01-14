from database.decorators.dict_cursor_decorator import dict_cursor


@dict_cursor
def get_driver_info_action(cursor, user_id):
    cursor.execute("SELECT * FROM drivers WHERE id = %s", (user_id,))

    return cursor.fetchone()
