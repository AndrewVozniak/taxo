def update_action(cursor, table, column, value, user_id):
    try:
        cursor.execute(f"UPDATE {table} SET {column} = %s WHERE id = %s", (value, user_id))
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return False
