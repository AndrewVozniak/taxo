from translations.core import translations, get_language
from database.actions import create_passenger


def init(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_name"])
    bot.register_next_step_handler(message, enter_name_stage, bot, cursor, user_id)


def enter_name_stage(message, bot, cursor, user_id):
    name = message.text
    passenger = create_passenger.create_passenger_action(cursor, user_id, name)

    if passenger is None:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["errors"]["unknown"])
        return

    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["success_register"])
