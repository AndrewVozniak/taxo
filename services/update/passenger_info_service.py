from keyboards.core import yes_no_keyboard
from translations.core import translations, get_language
from telebot import types


def edit_name(bot, message, cursor, user_id):
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["edit_name"]["message"])

    bot.register_next_step_handler(message, edit_name_step, bot, cursor, user_id)


def edit_name_step(message, bot, cursor, user_id):
    from database.actions.update_row import update_action

    update_action(cursor, "passengers", "name", message.text, user_id)

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["edit_name"]["success"])
    return


def delete_user(bot, message, cursor, user_id):
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["delete_profile"]["message"],
                     reply_markup=yes_no_keyboard(user_id))

    bot.register_next_step_handler(message, delete_user_step, bot, cursor, user_id)


def delete_user_step(message, bot, cursor, user_id):
    if message.text == translations[get_language(user_id=user_id)]["yes"]:
        from database.actions.delete_row import delete_action

        delete_action(cursor, "passengers", user_id)

        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["delete_profile"]["success"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    elif message.text == translations[get_language(user_id=user_id)]["no"]:
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["delete_profile"]["cancel"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    else:
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["errors"]["choose_from_list"])
        return
