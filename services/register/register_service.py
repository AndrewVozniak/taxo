import time

from services import change_language_service

from translations.core import get_language, translations
from keyboards.core import choose_profile_type_keyboard


def init(bot, message, cursor, user_id):
    change_language_service.init(bot, message, user_id)

    bot.register_next_step_handler(message, choose_profile_type_stage, bot, cursor, user_id)


def choose_profile_type_stage(message, bot, cursor, user_id):
    # минимальная задержка чтобы сначала всегда отправлялось первым сообщение об успешном выборе языка
    time.sleep(0.3)

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["choose_profile_type"]["message"],
                     reply_markup=choose_profile_type_keyboard(user_id))

    bot.register_next_step_handler(message, branch_stage, bot, cursor, user_id)


def branch_stage(message, bot, cursor, user_id):
    if message.text == translations[get_language(user_id=user_id)]["choose_profile_type"]["profile_types"]["passenger"]:
        from services.register import register_passenger_service
        register_passenger_service.init(bot, message, cursor, user_id)
        return

    elif message.text == translations[get_language(user_id=user_id)]["choose_profile_type"]["profile_types"]["driver"]:
        from services.register import register_driver_service
        register_driver_service.init(bot, message, cursor, user_id)
        return

    else:
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["choose_profile_type"]["error"])

        bot.register_next_step_handler(message, branch_stage, bot, cursor, user_id)
