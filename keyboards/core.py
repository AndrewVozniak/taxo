from telebot import types
from keyboards.buttons import register, main_menu_driver, main_menu_passenger, main_menu_my_profile_passenger, main_menu_my_profile_driver
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


def main_menu_keyboard(user_id, user_type, is_active=False):
    keyboard = types.InlineKeyboardMarkup()

    if user_type == "passenger":
        [keyboard.add(btn) for btn in main_menu_passenger.init(user_id)]

    elif user_type == "driver":
        [keyboard.add(btn) for btn in main_menu_driver.init(user_id)]

        if is_active:
            keyboard.add(types.InlineKeyboardButton(
                text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["driver"]["go_offline"],
                callback_data="go_offline"
            ))

        else:
            keyboard.add(types.InlineKeyboardButton(
                text=translations[get_language(user_id=user_id)]["keyboards"]["main_menu"]["driver"]["go_online"],
                callback_data="go_online"
            ))

    return keyboard


def passenger_my_profile_menu_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()

    [keyboard.add(btn) for btn in main_menu_my_profile_passenger.init(user_id)]

    return keyboard


def driver_my_profile_menu_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()

    [keyboard.add(btn) for btn in main_menu_my_profile_driver.init(user_id)]

    return keyboard
