from translations.core import set_temporary_language, get_language, translations
from keyboards.core import change_language_keyboard
from telebot import types


def init(bot, message, user_id):
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["change_language"]["message"],
                     reply_markup=change_language_keyboard())
    bot.register_next_step_handler(message, change_language, bot)


def change_language(message, bot):
    if message.text == "🇷🇺 Русский":
        set_temporary_language(user_id=message.from_user.id, language="ru")
    elif message.text == "🇺🇸 English":
        set_temporary_language(user_id=message.from_user.id, language="en")
    else:
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=message.from_user.id)]["change_language"]["error"])
        bot.register_next_step_handler(message, change_language, bot)
        return

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=message.from_user.id)]["change_language"]["success"],
                     reply_markup=types.ReplyKeyboardRemove())
