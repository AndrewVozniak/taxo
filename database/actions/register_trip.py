def register_trip_action(cursor,
                         passenger_id, driver_id,
                         passenger_count, has_luggage,
                         has_child_seat,
                         pickup_location, dropoff_location,
                         requested_at, confirmed_at):
    status = 'waiting'

    cursor.execute("INSERT INTO trips (passenger_id, driver_id, passenger_count, has_luggage, has_child_seat, "
                   "pickup_location, dropoff_location, status, requested_at, confirmed_at) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (passenger_id, driver_id, passenger_count, has_luggage, has_child_seat, pickup_location,
                    dropoff_location, status, requested_at, confirmed_at))

    cursor.connection.commit()

