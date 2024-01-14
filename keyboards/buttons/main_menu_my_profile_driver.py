from telebot import types
from translations.core import translations, get_language


def init(user_id):
    return [
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["driver_my_profile_menu"]["edit_data"],
            callback_data="driver_my_profile_menu_edit_data"
        ),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["driver_my_profile_menu"]["delete_profile"],
            callback_data="driver_my_profile_menu_delete_profile"
        ),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["driver_my_profile_menu"]["change_language"],
            callback_data="change_language"
        ),
        types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["driver_my_profile_menu"]["back"],
            callback_data="main_menu"
        ),
    ]
