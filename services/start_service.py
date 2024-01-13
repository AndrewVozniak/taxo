from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from keyboards.core import register_keyboard
from services import menu_service


def init(bot, message, cursor, user_id):
    try:
        user = get_user_base_info_action(cursor, user_id)

        if user is None:
            bot.send_message(message.chat.id,
                             translations[get_language(user_id=user_id)]["errors"]["not_registered"],
                             reply_markup=register_keyboard(user_id))
            return

        menu_service.main_menu(bot, message, cursor, user_id)
        return

    except Exception as e:
        bot.send_message(message.chat.id,
                         translations[get_language(get_language(user_id=user_id))]["errors"]["unknown"])
        print(e)
        return
