def dict_cursor(func):
    def wrapper(cursor, *args, **kwargs):
        result = func(cursor, *args, **kwargs)
        if result is not None:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, result))
        return None

    return wrapper
