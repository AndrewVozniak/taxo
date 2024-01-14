def create_driver_action(cursor, id, name, car_brand, seating_capacity, has_child_seat, about):
    try:
        cursor.execute("INSERT INTO drivers (id, name, car_brand, seating_capacity, has_child_seat, about) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (id, name, car_brand, seating_capacity, has_child_seat, about))
        cursor.connection.commit()

        return {
            "id": id,
            "name": name,
            "car_brand": car_brand,
            "seating_capacity": seating_capacity,
            "has_child_seat": has_child_seat,
            "about": about
        }
    except Exception as e:
        print(e)

        return None
