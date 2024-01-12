import telebot
import config

from database import connector

from services import start_service

bot = telebot.TeleBot(config.bot_config["token"])
connection, cursor = connector.init(
    config.database_config["host"],
    config.database_config["db"],
    config.database_config["user"],
    config.database_config["password"]
)


@bot.message_handler(commands=["start"])
def start(message):
    start_service.start(bot, message, cursor)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "register":
        bot.send_message(call.message.chat.id, "Register")


bot.polling(none_stop=True)
