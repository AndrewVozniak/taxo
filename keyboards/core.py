from telebot import types
from keyboards.buttons import register, main_menu_driver, main_menu_passenger
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


def yes_no_keyboard(user_id):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(translations[get_language(user_id=user_id)]["yes"])
    keyboard.row(translations[get_language(user_id=user_id)]["no"])

    return keyboard


def main_menu_keyboard(user_id, user_type):
    keyboard = types.InlineKeyboardMarkup()

    if user_type == "passenger":
        [keyboard.add(btn) for btn in main_menu_passenger.init(user_id)]

    elif user_type == "driver":
        [keyboard.add(btn) for btn in main_menu_driver.init(user_id)]

    return keyboard


def passenger_my_profile_menu_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(
        text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"]["edit_name"],
        callback_data="passenger_my_profile_menu_edit_name"))
    keyboard.add(types.InlineKeyboardButton(
        text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"]["change_language"],
        callback_data="change_language"))
    keyboard.add(types.InlineKeyboardButton(
        text=translations[get_language(user_id=user_id)]["keyboards"]["passenger_my_profile_menu"]["back"],
        callback_data="main_menu"))

    return keyboard
