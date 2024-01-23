def is_admin(cursor, user_id):
    try:
        cursor.execute("SELECT * FROM admins WHERE id = %s", (user_id,))
        data = cursor.fetchone()

        if data:
            return True

    except AttributeError as e:
        print(e)
        return False
