from telebot import types


def btns():
    return [
        types.InlineKeyboardButton(text="Register", callback_data="change_language")
    ]
