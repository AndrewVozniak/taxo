from telebot import types

import config
from database.actions.get_user_base_info import get_user_base_info_action
from translations.core import translations, get_language


def init(bot, cursor, message, user_id):
    user = get_user_base_info_action(cursor, user_id)

    if user is None:
        bot.send_message(message.chat.id, translations[get_language(user_id)]["errors"]["unknown"])
        return

    if user['type'] == 'passenger':
        bot.send_message(message.chat.id, translations[get_language(user_id)]["charity"]["passenger"])
        return

    if user['type'] == 'driver':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id)]["keyboards"]["feedback"],
            callback_data="send_feedback"
        ))

        bot.send_message(message.chat.id,
                         translations[get_language(user_id)]["charity"]["driver"].format(
                             charity_wallet=config.CHARITY_WALLET),
                         reply_markup=keyboard)
        return


def send_feedback(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id)]["charity"]["send_feedback"])
    bot.register_next_step_handler(message, send_feedback_action, bot, cursor, user_id)


def send_feedback_action(message, bot, cursor, user_id):
    cursor.execute("INSERT INTO feedbacks (user_id, feedback) VALUES (%s, %s)", (user_id, message.text))
    cursor.connection.commit()

    bot.send_message(message.chat.id, translations[get_language(user_id)]["charity"]["feedback_sent"])
