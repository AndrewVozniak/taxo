from translations.core import translations, default_language
from database.actions.get_user_base_info import get_user_base_info_action
from keyboards.core import register_keyboard


def start(bot, message, cursor):
    user_id = message.from_user.id

    try:
        user = get_user_base_info_action(cursor, user_id)

        if user is None:
            bot.send_message(message.chat.id, translations[default_language]["errors"]["not_registered"],
                             reply_markup=register_keyboard())
            return

        bot.send_message(message.chat.id, "Hello, world!")

    except Exception as e:
        bot.send_message(message.chat.id, translations[default_language]["errors"]["unknown"])
        print(e)
        return
