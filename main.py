import telebot
import config

from database import connector
from services import start_service, change_language_service, menu_service, search_service, call_service
from services.register import register_service
from services.update import passenger_info_service, driver_info_service

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
    start_service.init(bot, message, cursor, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "register":
        register_service.init(bot, call.message, cursor, call.from_user.id)

    elif call.data == "main_menu":
        menu_service.main_menu(bot, call.message, cursor, call.from_user.id)

    elif call.data == "change_language":
        change_language_service.init(bot, call.message, call.from_user.id)

    elif call.data == "get_nearby_drivers_count":
        search_service.get_nearby_drivers_count(bot, call.message, cursor, call.from_user.id)

    # ! PASSENGER
    elif call.data == "main_menu_passenger_my_profile":
        menu_service.passenger_my_profile_menu(bot, call.message, cursor, call.from_user.id)

    elif call.data == "passenger_my_profile_menu_edit_name":
        passenger_info_service.edit_name(bot, call.message, cursor, call.from_user.id)

    elif call.data == "passenger_my_profile_menu_delete_profile":
        passenger_info_service.delete_user(bot, call.message, cursor, call.from_user.id)

    elif call.data == "main_menu_passenger_call_taxi":
        call_service.init(bot, call.message, cursor, call.from_user.id)

    elif call.data == "main_menu_passenger_book_taxi":
        call_service.init(bot, call.message, cursor, call.from_user.id, True)

    elif call.data == "cancel_trip":
        call_service.cancel_trip(bot, call.message, cursor, call.from_user.id)

    elif call.data.startswith("call_driver_"):
        call_service.choose_driver(bot, call.message, cursor, call.from_user.id, call.data.split("_")[2])

    elif call.data.startswith("submit_trip"):
        call_service.submit(bot, call.message, cursor, call.from_user.id, call.data.split("_")[2])

    # ! DRIVER
    elif call.data == "main_menu_driver_my_profile":
        menu_service.driver_my_profile_menu(bot, call.message, cursor, call.from_user.id)

    elif call.data == "driver_my_profile_menu_edit_data":
        driver_info_service.edit_data(bot, call.message, cursor, call.from_user.id)

    elif call.data == "driver_my_profile_menu_delete_profile":
        driver_info_service.delete_profile(bot, call.message, cursor, call.from_user.id)

    elif call.data == "main_menu_driver_set_my_geo_position":
        driver_info_service.set_my_geo_position(bot, call.message, cursor, call.from_user.id)

    elif call.data == "go_online":
        driver_info_service.go_online(bot, call.message, cursor, call.from_user.id)

    elif call.data == "go_offline":
        driver_info_service.go_offline(bot, call.message, cursor, call.from_user.id)

    elif call.data == "im_arrived":
        call_service.im_arrived(bot, call.message, cursor, call.from_user.id)

    elif call.data == "start_trip":
        call_service.start_trip(bot, call.message, cursor, call.from_user.id)

    elif call.data == "end_trip":
        call_service.end_trip(bot, call.message, cursor, call.from_user.id)

    elif call.data.startswith("sub_booking"):
        call_service.submit_booking(bot, call.message, cursor, call.from_user.id, call.data.split("_")[2])


bot.polling(none_stop=True)
