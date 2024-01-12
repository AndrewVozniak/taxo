from telebot import types
from keyboards.buttons import register
from translations.core import get_language, translations


def register_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    [keyboard.add(btn) for btn in register.init(user_id)]
    return keyboard


def change_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("🇷🇺 Русский", "🇺🇸 English")

    return keyboard


def choose_profile_type_keyboard(user_id):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(translations[get_language(user_id=user_id)]["choose_profile_type"]["profile_types"]["passenger"])
    keyboard.row(translations[get_language(user_id=user_id)]["choose_profile_type"]["profile_types"]["driver"])

    return keyboard
