from helpers.get_nearby_drivers import get_nearby_drivers
from database.actions.get_user_base_info import get_user_base_info_action
from database.actions.get_driver_location import get_driver_location_action
from translations.core import get_language, translations
from services.update.driver_info_service import set_my_geo_position
from config import DEFAULT_SEARCH_RADIUS


def get_nearby_drivers_count(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)

    if user["type"] == "driver":
        user["current_location"] = get_driver_location_action(cursor, user_id)["current_location"]

        if user["current_location"] is None:
            return set_my_geo_position(bot, message, cursor, user_id)

        lat, lon = user["current_location"].split(",")

        drivers = get_nearby_drivers(cursor,
                                     user_id,
                                     lat,
                                     lon,
                                     DEFAULT_SEARCH_RADIUS)
        drivers_count = len(drivers)

        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["nearby_drivers_count"]["message"].format(
                count=drivers_count
            ),
        )
        return

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["nearby_drivers_count"]["send_location"],
        )
        bot.register_next_step_handler(message, get_nearby_passenger_drivers_count_stage, bot, cursor, user_id)


def get_nearby_passenger_drivers_count_stage(message, bot, cursor, user_id):
    if message.location is None:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["set_my_geo_position"]["error"],
        )
        return

    lat, lon = message.location.latitude, message.location.longitude

    drivers = get_nearby_drivers(cursor,
                                 user_id,
                                 lat,
                                 lon,
                                 DEFAULT_SEARCH_RADIUS)

    drivers_count = len(drivers)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["nearby_drivers_count"]["message"].format(
            count=drivers_count
        ),
    )
    return
