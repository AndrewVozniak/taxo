def get_user_base_info_action(cursor, user_id):
    cursor.execute("""
        (SELECT name FROM passengers WHERE id = %s)
        UNION
        (SELECT name FROM drivers WHERE id = %s)
    """, (user_id, user_id))

    return cursor.fetchone()