from telebot import types
from translations.core import translations, get_language


def init(user_id):
    return [
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["driver"]["my_profile"],
            callback_data="main_menu_driver_my_profile"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["driver"]["set_my_geo_position"],
            callback_data="main_menu_driver_set_my_geo_position"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["driver"]["get_nearby_drivers_count"],
            callback_data="get_nearby_drivers_count"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["get_charity_wallet"],
            callback_data="get_charity_wallet")
        ]

