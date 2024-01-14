def delete_action(cursor, table, id):
    try:
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (id,))
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return False
