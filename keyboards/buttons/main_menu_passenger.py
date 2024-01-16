from telebot import types
from translations.core import translations, get_language


def init(user_id):
    return [
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["passenger"]["my_profile"],
            callback_data="main_menu_passenger_my_profile"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["passenger"]["call_taxi"],
            callback_data="main_menu_passenger_call_taxi"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["passenger"]["book_taxi"],
            callback_data="main_menu_passenger_book_taxi"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["passenger"][
                "get_nearby_drivers_count"],
            callback_data="get_nearby_drivers_count")
    ]
