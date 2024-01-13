import telebot
import config

from database import connector
from services import start_service, change_language_service, menu_service
from services.register import register_service

bot = telebot.TeleBot(config.bot_config["token"])
connection, cursor = connector.init(
    config.database_config["host"],
    config.database_config["db"],
    config.database_config["user"],
    config.database_config["password"]
)


@bot.message_handler(commands=["start"])
def start(message):
    start_service.init(bot, message, cursor, message.from_user.id)


@bot.message_handler(content_types=["text"])
def text(message):
    menu_service.main_menu(bot, message, cursor, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "register":
        register_service.init(bot, call.message, cursor, call.from_user.id)

    elif call.data == "main_menu":
        menu_service.main_menu(bot, call.message, cursor, call.from_user.id)

    elif call.data == "change_language":
        change_language_service.init(bot, call.message, call.from_user.id)

    elif call.data == "main_menu_passenger_my_profile":
        menu_service.passenger_my_profile_menu(bot, call.message, cursor, call.from_user.id)


bot.polling(none_stop=True)
