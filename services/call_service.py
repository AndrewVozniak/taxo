import keyboards.core
from config import DEFAULT_WAITING_TIME_OUT, DEFAULT_ARRIVAL_TIME_OUT
from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from database.actions.register_trip import register_trip_action
from database.actions.update_row import update_action
from keyboards.core import yes_no_keyboard
from telebot import types
from helpers.get_nearby_drivers import get_nearby_drivers_by_filters
from temporary_storages.main import unapproved_calls
from helpers.get_info_by_coordinates import get_info_by_coordinates
from datetime import datetime, timedelta
from jobs.main import scheduler, cancel_call_if_not_confirmed, show_cancel_button_if_arrival_time_too_long
from database.actions.get_trip_details_by_passenger_id import get_trip_details_by_passenger_id_action
from database.actions.get_trip_details_by_driver_id import get_trip_details_by_driver_id_action


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


def choose_driver(bot, message, cursor, user_id, driver_id):
    try:
        call = unapproved_calls[user_id]
    except KeyError:
        print("Call not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    try:
        if call["driver_id"] is not None:
            print("Driver already chosen")
            bot.send_message(
                chat_id=message.chat.id,
                text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
            )
            return
    except KeyError:
        pass

    driver_id = int(driver_id)
    call["driver_id"] = driver_id
    call["requested_at"] = datetime.now()

    scheduler.add_job(func=cancel_call_if_not_confirmed,
                      id='cancel_call_if_not_confirmed',
                      run_date=datetime.now() + timedelta(seconds=DEFAULT_WAITING_TIME_OUT),
                      args=[bot, cursor, user_id])

    user = get_user_base_info_action(cursor, user_id)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=translations[get_language(user_id=driver_id)]["keyboards"]["call_driver"]["submit"],
        callback_data=f"submit_trip_{driver_id}",
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


def submit(bot, message, cursor, user_id, driver_id):
    call = None
    passenger_id = None

    for key, unapproved_call in unapproved_calls.items():
        if int(unapproved_call["driver_id"]) == int(driver_id):
            call = unapproved_call
            passenger_id = key
            break

    if call is None:
        print("Call not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    try:
        if call["confirmed_at"] is not None:
            print("Call already confirmed")
            bot.send_message(
                chat_id=message.chat.id,
                text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
            )
            return
    except KeyError:
        pass

    call["confirmed_at"] = datetime.now()

    scheduler.remove_job('cancel_call_if_not_confirmed')
    scheduler.add_job(func=show_cancel_button_if_arrival_time_too_long,
                      id='show_cancel_button_if_arrival_time_too_long',
                      run_date=datetime.now() + timedelta(seconds=DEFAULT_ARRIVAL_TIME_OUT),
                      args=[bot, cursor, passenger_id])

    call["location"] = f"{call['location'].latitude},{call['location'].longitude}"
    call["destination"] = f"{call['destination'].latitude},{call['destination'].longitude}"

    register_trip_action(cursor=cursor,
                         passenger_id=passenger_id,
                         driver_id=driver_id,
                         passenger_count=call["passengers_count"],
                         has_luggage=call["baggage"],
                         has_child_seat=call["child_seat"],
                         pickup_location=call["location"],
                         dropoff_location=call["destination"],
                         requested_at=call["requested_at"],
                         confirmed_at=call["confirmed_at"])

    bot.send_message(
        chat_id=user_id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["trip_accepted_driver"].format(
            name=get_user_base_info_action(cursor, user_id)["name"],
        ),
        reply_markup=keyboards.core.im_arrived_keyboard(user_id)
    )

    bot.send_message(
        chat_id=passenger_id,
        text=translations[get_language(user_id=passenger_id)]["call_driver"]["trip_accepted_passenger"].format(
            name=get_user_base_info_action(cursor, driver_id)["name"],
        ),
    )

    del unapproved_calls[passenger_id]


def im_arrived(bot, message, cursor, user_id):
    trip = get_trip_details_by_driver_id_action(cursor, user_id)

    if trip is None:
        print("Trip not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    if trip["status"] != "waiting":
        print("Trip status is not en_route")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    try:
        scheduler.remove_job('show_cancel_button_if_arrival_time_too_long')
    except Exception as e:
        print(e)

    if trip is None:
        print("Trip not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    update_action(cursor, "trips", "status", "driver_arrived", trip["id"])

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["driver_arrived_driver"],
        reply_markup=keyboards.core.start_trip_keyboard(user_id)
    )

    bot.send_message(
        chat_id=trip["passenger_id"],
        text=translations[get_language(user_id=trip["passenger_id"])]["call_driver"]["driver_arrived_passenger"],
    )


def start_trip(bot, message, cursor, user_id):
    trip = get_trip_details_by_driver_id_action(cursor, user_id)

    if trip is None:
        print("Trip not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    if trip["status"] != "driver_arrived":
        print("Trip status is not driver_arrived")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    update_action(cursor, "trips", "status", "en_route", trip["id"])

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["trip_started_driver"],
        reply_markup=keyboards.core.end_trip_keyboard(user_id)
    )

    bot.send_message(
        chat_id=trip["passenger_id"],
        text=translations[get_language(user_id=trip["passenger_id"])]["call_driver"]["trip_started_passenger"],
    )


def end_trip(bot, message, cursor, user_id):
    trip = get_trip_details_by_driver_id_action(cursor, user_id)

    if trip is None:
        print("Trip not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    if trip["status"] != "en_route":
        print("Trip status is not en_route")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    update_action(cursor, "trips", "status", "completed", trip["id"])
    update_action(cursor, "trips", "completed_at", datetime.now(), trip["id"])

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["trip_ended"],
    )

    bot.send_message(
        chat_id=trip["passenger_id"],
        text=translations[get_language(user_id=trip["passenger_id"])]["call_driver"]["trip_ended"],
    )


def cancel_trip(bot, message, cursor, user_id):
    trip = get_trip_details_by_passenger_id_action(cursor, user_id)

    if trip is None:
        print("Trip not found")
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    if trip["status"] != "waiting":
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["call_driver"]["cant_cancel"],
        )
        return

    update_action(cursor, "trips", "status", "cancelled", trip["id"])

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["you_cancel"],
    )

    bot.send_message(
        chat_id=trip["driver_id"],
        text=translations[get_language(user_id=trip["driver_id"])]["call_driver"]["trip_canceled"],
    )
