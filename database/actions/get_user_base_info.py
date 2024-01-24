from database.decorators.dict_cursor_decorator import dict_cursor


@dict_cursor
def get_user_base_info_action(cursor, user_id):
    cursor.execute("""
        SELECT 'passenger' AS type, name, rating FROM passengers WHERE id = %s
        UNION
        SELECT 'driver' AS type, name, rating FROM drivers WHERE id = %s
    """, (user_id, user_id))

    return cursor.fetchone()
