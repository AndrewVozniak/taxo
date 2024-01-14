from telebot import types
from translations.core import translations, get_language


def init(user_id):
    return [
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"]["edit_name"],
            callback_data="passenger_my_profile_menu_edit_name"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"][
                "change_language"],
            callback_data="change_language"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"][
                "delete_profile"],
            callback_data="passenger_my_profile_menu_delete_profile"),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"]["back"],
            callback_data="main_menu")
    ]
