from telebot import types
from translations.core import translations, get_language


def init(user_id):
    return [
        types.InlineKeyboardButton(text=translations[get_language(user_id=user_id)]["keyboards"]["register"]["register"],
                                   callback_data="register")
    ]
