from database.decorators.dict_cursor_decorator import dict_cursor_all


@dict_cursor_all
def get_drivers_location_action(cursor):
    cursor.execute("SELECT id, is_active, current_location FROM drivers")

    return cursor.fetchall()
