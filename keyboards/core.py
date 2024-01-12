from telebot import types
from keyboards.buttons import register


def register_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    [keyboard.add(btn) for btn in register.btns()]
    return keyboard
