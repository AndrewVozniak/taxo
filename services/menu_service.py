from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from database.actions.get_driver_info import get_driver_info_action
from database.actions.get_driver_status import get_driver_status_action
from keyboards.core import main_menu_keyboard, passenger_my_profile_menu_keyboard, driver_my_profile_menu_keyboard
from helpers.get_info_by_coordinates import get_info_by_coordinates


def main_menu(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)
    user["is_active"] = False

    if user["type"] == "driver":
        user["is_active"] = get_driver_status_action(cursor, user_id)["is_active"]

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
                     reply_markup=main_menu_keyboard(user_id, user["type"], user["is_active"]))


def passenger_my_profile_menu(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["menus"]["passenger_my_profile_menu"][
                         "message"].format(user["name"]),
                     reply_markup=passenger_my_profile_menu_keyboard(user_id))


def driver_my_profile_menu(bot, message, cursor, user_id):
    user = get_driver_info_action(cursor, user_id)

    if user["is_active"]:
        user["is_active"] = translations[get_language(user_id=user_id)]["yes"]

    else:
        user["is_active"] = translations[get_language(user_id=user_id)]["no"]

    if user["has_child_seat"]:
        user["has_child_seat"] = translations[get_language(user_id=user_id)]["yes"]

    else:
        user["has_child_seat"] = translations[get_language(user_id=user_id)]["no"]

    if user["current_location"] is None:
        user["current_location"] = translations[get_language(user_id=user_id)]["undefined"]

    else:
        try:
            lat, lon = user["current_location"].split(",")
            user["current_location"] = get_info_by_coordinates(lat, lon)

        except ValueError:
            user["current_location"] = translations[get_language(user_id=user_id)]["undefined"]

    if user["active_radius"] is None:
        user["active_radius"] = translations[get_language(user_id=user_id)]["undefined"]

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["menus"]["driver_my_profile_menu"][
                         "message"].format(
                         name=user.get('name', translations[get_language(user_id=user_id)]["undefined"]),
                         car_brand=user.get('car_brand', translations[get_language(user_id=user_id)]["undefined"]),
                         seating_capacity=user.get('seating_capacity',
                                                   translations[get_language(user_id=user_id)]['undefined']),

                         has_child_seat=user.get('has_child_seat',
                                                 translations[get_language(user_id=user_id)]["undefined"]),

                         about=user.get('about', translations[get_language(user_id=user_id)]["undefined"]),

                         geo_position=user.get('current_location',
                                               translations[get_language(user_id=user_id)]["undefined"]),

                         active_radius=user.get('active_radius',
                                                translations[get_language(user_id=user_id)]["undefined"]),

                         is_active=user.get('is_active', translations[get_language(user_id=user_id)]["no"]),
                     ),
                     reply_markup=driver_my_profile_menu_keyboard(user_id))
