from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from keyboards.core import main_menu_keyboard, passenger_my_profile_menu_keyboard


def main_menu(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
                     reply_markup=main_menu_keyboard(user_id, user["type"]))


def passenger_my_profile_menu(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)

    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["menus"]["passenger_my_profile_menu"][
                         "message"].format(user["name"]),
                     reply_markup=passenger_my_profile_menu_keyboard(user_id))
