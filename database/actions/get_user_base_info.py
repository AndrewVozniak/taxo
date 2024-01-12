def get_user_base_info_action(cursor, user_id):
    cursor.execute("""
        (SELECT name, language FROM passengers WHERE id = %s)
        UNION
        (SELECT name, language FROM drivers WHERE id = %s)
    """, (user_id, user_id))

    return cursor.fetchone()