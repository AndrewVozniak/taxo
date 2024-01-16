from database.actions.get_drivers_search_data import get_drivers_search_data_action
from helpers.get_distance import get_distance
from database.actions.get_driver_info import get_driver_info_action
from config import DEFAULT_SEARCH_RADIUS
from translations.core import translations, get_language

def get_nearby_drivers(cursor, user_id, lat, lon, radius=DEFAULT_SEARCH_RADIUS, use_default_radius=True):
    """
    :param use_default_radius:
    :param cursor: database cursor
    :param user_id: user id
    :param lat: latitude
    :param lon: longitude
    :param radius: radius in km
    :return: list of nearby taxis
    """
    nearby_taxis = []
    drivers = get_drivers_search_data_action(cursor)

    for driver in drivers:
        if driver["is_active"] and driver["id"] != user_id:
            try:
                driver_lat, driver_lon = driver["current_location"].split(",")
                distance = get_distance(lat, lon, float(driver_lat), float(driver_lon))

                # учитываем радиус действия водителя и дефолтный радиус поиска (во избежание шутников с 10000 км)
                if distance <= driver["active_radius"]:
                    if use_default_radius:
                        if distance <= radius:
                            nearby_taxis.append(driver)
                    else:
                        nearby_taxis.append(driver)

            except ValueError:
                pass

    return nearby_taxis


def get_nearby_drivers_by_filters(cursor, user_id, location, passengers_count, child_seat):
    nearby_drivers = get_nearby_drivers(cursor, user_id,
                                        location.latitude, location.longitude,
                                        DEFAULT_SEARCH_RADIUS, False)
    filtered_drivers = []

    for driver in nearby_drivers:
        driver = get_driver_info_action(cursor, driver["id"])

        driver_lat, driver_lon = driver["current_location"].split(",")

        if driver["seating_capacity"] >= passengers_count:
            if child_seat:
                if driver["has_child_seat"]:
                    filtered_drivers.append({
                        "driver_id": driver["id"],
                        "name": driver["name"],
                        "car_brand": driver["car_brand"],
                        "has_child_seat": translations[get_language(user_id=user_id)]["yes"],
                        "about": driver["about"],
                        "distance": get_distance(location.latitude, location.longitude,
                                                 float(driver_lat), float(driver_lon)),
                    })
            else:
                filtered_drivers.append({
                    "driver_id": driver["id"],
                    "name": driver["name"],
                    "car_brand": driver["car_brand"],
                    "has_child_seat": translations[get_language(user_id=user_id)]["no"],
                    "about": driver["about"],
                    "distance": get_distance(location.latitude, location.longitude,
                                             float(driver_lat), float(driver_lon)),
                })

    return filtered_drivers
