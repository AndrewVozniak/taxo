from database.actions.get_drivers_location import get_drivers_location_action


def get_distance(lat1, lon1, lat2, lon2):
    """
    :param lat1: latitude of point 1
    :param lon1: longitude of point 1
    :param lat2: latitude of point 2
    :param lon2: longitude of point 2
    :return: distance between two points in km
    """
    from math import sin, cos, sqrt, atan2, radians

    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)

    # approximate radius of earth in km
    R = 6373.0

    # convert degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # calculate difference between latitudes and longitudes
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # calculate distance between two points
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(R * c, 2)


def get_nearby_drivers(cursor, user_id, lat, lon, radius):
    """
    :param cursor: database cursor
    :param lat: latitude
    :param lon: longitude
    :param radius: radius in km
    :return: list of nearby taxis
    """
    nearby_taxis = []
    drivers = get_drivers_location_action(cursor)

    for driver in drivers:
        if driver["is_active"] and driver["id"] != user_id:
            try:
                driver_lat, driver_lon = driver["current_location"].split(",")
                distance = get_distance(lat, lon, float(driver_lat), float(driver_lon))

                if distance <= radius:
                    nearby_taxis.append(driver)

            except ValueError:
                pass

    return nearby_taxis
