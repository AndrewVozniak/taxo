from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from keyboards.core import yes_no_keyboard
from telebot import types
from helpers.get_nearby_drivers import get_nearby_drivers_by_filters
from temporary_storages.unapproved_calls import unapproved_calls
from helpers.get_info_by_coordinates import get_info_by_coordinates


def init(bot, message, cursor, user_id):
    user = get_user_base_info_action(cursor, user_id)

    if user is None or user["type"] != "passenger":
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["send_location"])

    bot.register_next_step_handler(message, get_location_stage, bot, cursor, user_id)


def get_location_stage(message, bot, cursor, user_id):
    if message.location is None:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_location"],
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["send_destination"],
    )

    bot.register_next_step_handler(message, get_destination_stage, bot, cursor, user_id, message.location)


def get_destination_stage(message, bot, cursor, user_id, location):
    if message.location is None:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_location"],
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["send_passengers_count"],
    )

    bot.register_next_step_handler(message, get_passengers_count_stage, bot, cursor, user_id, location,
                                   message.location)


def get_passengers_count_stage(message, bot, cursor, user_id, location, destination):
    if not message.text.isdigit():
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_number"],
        )
        bot.register_next_step_handler(message, get_passengers_count_stage, bot, cursor, user_id, location,
                                       destination)
        return

    passengers_count = int(message.text)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["do_you_have_baggage"],
        reply_markup=yes_no_keyboard(user_id=message.from_user.id),
    )

    bot.register_next_step_handler(message, get_baggage_stage, bot, cursor, user_id, location, destination,
                                   passengers_count)


def get_baggage_stage(message, bot, cursor, user_id, location, destination, passengers_count):
    if message.text not in [translations[get_language(user_id=user_id)]["yes"],
                            translations[get_language(user_id=user_id)]["no"]]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["choose_from_list"],
            reply_markup=yes_no_keyboard(user_id=message.from_user.id),
        )
        bot.register_next_step_handler(message, get_baggage_stage, bot, cursor, user_id, location, destination,
                                       passengers_count)
        return

    baggage = message.text == translations[get_language(user_id=user_id)]["yes"]

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["do_you_need_child_seat"],
        reply_markup=yes_no_keyboard(user_id=message.from_user.id),
    )

    bot.register_next_step_handler(message, get_child_seat_stage, bot, cursor, user_id, location, destination,
                                   passengers_count, baggage)


def get_child_seat_stage(message, bot, cursor, user_id, location, destination, passengers_count, baggage):
    if message.text not in [translations[get_language(user_id=user_id)]["yes"],
                            translations[get_language(user_id=user_id)]["no"]]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["choose_from_list"],
            reply_markup=yes_no_keyboard(user_id=message.from_user.id),
        )
        bot.register_next_step_handler(message, get_child_seat_stage, bot, cursor, user_id, location, destination,
                                       passengers_count, baggage)
        return

    child_seat = message.text == translations[get_language(user_id=user_id)]["yes"]

    drivers = get_nearby_drivers_by_filters(cursor, user_id, location, passengers_count, child_seat)

    if len(drivers) == 0:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["no_drivers"],
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    unapproved_calls[user_id] = {
        "location": location,
        "destination": destination,
        "passengers_count": passengers_count,
        "baggage": baggage,
        "child_seat": child_seat,
        "submitted": False,
    }

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["drivers_list"],
        reply_markup=types.ReplyKeyboardRemove(),
    )

    drivers = drivers[:12]

    for driver in drivers:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["call_driver"]["choose_driver"],
            callback_data=f"call_driver_{driver['driver_id']}",
        ))

        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["driver_info"].format(
                name=driver["name"],
                car_brand=driver["car_brand"],
                has_child_seat=driver["has_child_seat"],
                about=driver["about"],
                distance=driver["distance"],
            ),
            reply_markup=keyboard,
        )

    # TODO: Отправка сообщения водителю о том что его выбрали с отправкой DESTINATION


def choose_driver(bot, message, cursor, user_id, driver_id):
    call = unapproved_calls[user_id]

    user = get_user_base_info_action(cursor, user_id)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=translations[get_language(user_id=user_id)]["keyboards"]["call_driver"]["submit"],
        callback_data=f"trip_submitted_{driver_id}",
    ))

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["you_choose_driver"]
    )

    bot.send_message(
        chat_id=driver_id,
        text=translations[get_language(user_id=driver_id)]["call_driver"]["you_were_chosen"].format(
            name=user["name"],
            location=get_info_by_coordinates(call["location"].latitude, call["location"].longitude),
            destination=get_info_by_coordinates(call["destination"].latitude, call["destination"].longitude),
            passengers_count=call["passengers_count"],
            baggage=translations[get_language(user_id=driver_id)]["yes"] if call["baggage"] else
            translations[get_language(user_id=driver_id)]["no"],
            child_seat=translations[get_language(user_id=driver_id)]["yes"] if call["child_seat"] else
            translations[get_language(user_id=driver_id)]["no"],
        ),
        reply_markup=keyboard
    )
