import random

import keyboards.core
from config import DEFAULT_WAITING_TIME_OUT, DEFAULT_ARRIVAL_TIME_OUT
from database.actions.get_driver_rating_info import get_driver_rating_info_action
from database.actions.get_passenger_rating_info import get_passenger_rating_info_action
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
from keyboards.core import cancel_keyboard
from helpers.block_user import block_user
from temporary_storages.main import unapproved_bookings


def init(bot, message, cursor, user_id, booking=False):
    from temporary_storages.main import failed_attempts_storage

    # Проверка блокировки пользователя
    if user_id in failed_attempts_storage:
        last_block_time = failed_attempts_storage[user_id]['last_block_time']
        if last_block_time:
            time_diff = datetime.now() - last_block_time
            if time_diff < timedelta(minutes=failed_attempts_storage[user_id]['block_duration']):
                bot.send_message(chat_id=message.chat.id,
                                 text=translations[get_language(user_id=user_id)]["you_have_been_blocked"].format(
                                     block_duration=failed_attempts_storage[user_id]['block_duration']))
                return

    user = get_user_base_info_action(cursor, user_id)

    if user is None or user["type"] != "passenger":
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["unknown"],
        )
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["call_driver"]["send_location"],
        reply_markup=cancel_keyboard(user_id),
    )

    bot.register_next_step_handler(message, get_location_stage, bot, cursor, user_id, booking)


def get_location_stage(message, bot, cursor, user_id, booking=False):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )
        return

    if message.location is None:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_location"],
            reply_markup=cancel_keyboard(user_id),
        )
        bot.register_next_step_handler(message, get_location_stage, bot, cursor, user_id, booking)
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["send_destination"],
        reply_markup=cancel_keyboard(user_id),
    )

    bot.register_next_step_handler(message, get_destination_stage, bot, cursor, user_id, message.location, booking)


def get_destination_stage(message, bot, cursor, user_id, location, booking):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )
        return

    if message.location is None:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_location"],
            reply_markup=cancel_keyboard(user_id),
        )
        bot.register_next_step_handler(message, get_destination_stage, bot, cursor, user_id, location, booking)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["send_passengers_count"],
        reply_markup=cancel_keyboard(user_id),
    )

    bot.register_next_step_handler(message, get_passengers_count_stage, bot, cursor, user_id, location,
                                   message.location, booking)


def get_passengers_count_stage(message, bot, cursor, user_id, location, destination, booking):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )
        return

    try:
        if not message.text.isdigit():
            bot.send_message(
                chat_id=message.chat.id,
                text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_number"],
                reply_markup=cancel_keyboard(user_id),
            )
            bot.register_next_step_handler(message, get_passengers_count_stage, bot, cursor, user_id, location,
                                           destination, booking)
            return
    except Exception as e:
        print(e)
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["enter_number"],
            reply_markup=cancel_keyboard(user_id),
        )
        bot.register_next_step_handler(message, get_passengers_count_stage, bot, cursor, user_id, location,
                                       destination, booking)
        return

    passengers_count = int(message.text)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["do_you_have_baggage"],
        reply_markup=yes_no_keyboard(user_id=message.from_user.id, with_cancel=True),
    )

    bot.register_next_step_handler(message, get_baggage_stage, bot, cursor, user_id, location, destination,
                                   passengers_count, booking)


def get_baggage_stage(message, bot, cursor, user_id, location, destination, passengers_count, booking):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )
        return

    if message.text not in [translations[get_language(user_id=user_id)]["yes"],
                            translations[get_language(user_id=user_id)]["no"]]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["choose_from_list"],
            reply_markup=yes_no_keyboard(user_id=message.from_user.id, with_cancel=True),
        )
        bot.register_next_step_handler(message, get_baggage_stage, bot, cursor, user_id, location, destination,
                                       passengers_count, booking)
        return

    baggage = message.text == translations[get_language(user_id=user_id)]["yes"]

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["do_you_need_child_seat"],
        reply_markup=yes_no_keyboard(user_id=message.from_user.id, with_cancel=True),
    )

    bot.register_next_step_handler(message, get_child_seat_stage, bot, cursor, user_id, location, destination,
                                   passengers_count, baggage, booking)


def get_child_seat_stage(message, bot, cursor, user_id, location, destination, passengers_count, baggage, booking):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )

        return

    if message.text not in [translations[get_language(user_id=user_id)]["yes"],
                            translations[get_language(user_id=user_id)]["no"]]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["errors"]["choose_from_list"],
            reply_markup=yes_no_keyboard(user_id=message.from_user.id, with_cancel=True),
        )
        bot.register_next_step_handler(message, get_child_seat_stage, bot, cursor, user_id, location, destination,
                                       passengers_count, baggage, booking)
        return

    child_seat = message.text == translations[get_language(user_id=user_id)]["yes"]

    drivers = get_nearby_drivers_by_filters(cursor, user_id, location, passengers_count, child_seat)

    if len(drivers) == 0:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["no_drivers"],
            reply_markup=types.ReplyKeyboardRemove(),
        )
        block_user(bot, message, user_id)

        return

    if booking is False:
        unapproved_calls[user_id] = {
            "location": location,
            "destination": destination,
            "passengers_count": passengers_count,
            "baggage": baggage,
            "child_seat": child_seat,
            "submitted": False,
            "passenger_username": message.from_user.username,
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
                    rating=driver["rating"],
                    car_brand=driver["car_brand"],
                    has_child_seat=driver["has_child_seat"],
                    about=driver["about"],
                    distance=driver["distance"],
                ),
                reply_markup=keyboard,
            )

    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["booking"]["send_date"],
            reply_markup=cancel_keyboard(user_id),
        )
        bot.register_next_step_handler(message, get_date_stage, bot, cursor, user_id, location, destination,
                                       passengers_count, baggage, child_seat)


def get_date_stage(message, bot, cursor, user_id, location, destination, passengers_count, baggage, child_seat):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )

        return

    date = message.text

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["booking"]["send_time"],
        reply_markup=cancel_keyboard(user_id),
    )
    bot.register_next_step_handler(message, get_time_stage, bot, cursor, user_id, location, destination,
                                   passengers_count, baggage, child_seat, date)


def get_time_stage(message, bot, cursor, user_id, location, destination, passengers_count, baggage, child_seat, date):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["action_canceled"],
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
            reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
        )

        return

    time = message.text

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["booking"]["booking_sent"],
        reply_markup=types.ReplyKeyboardRemove(),
    )

    drivers = get_nearby_drivers_by_filters(cursor, user_id, location, passengers_count, child_seat)

    if len(drivers) == 0:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=message.from_user.id)]["call_driver"]["no_drivers"],
            reply_markup=types.ReplyKeyboardRemove(),
        )
        return

    uniq_id = random.randint(1, 999999)
    hash_id = f"{user_id}{uniq_id}"

    unapproved_bookings[hash_id] = {
        "location": location,
        "destination": destination,
        "passengers_count": passengers_count,
        "baggage": baggage,
        "child_seat": child_seat,
        "date": date,
        "time": time,
        "submitted": False,
        "passenger_id": user_id,
        "passenger_username": message.from_user.username,
    }

    for i in range(len(drivers)):
        bot.send_message(
            chat_id=drivers[i]["driver_id"],
            text=translations[get_language(user_id=drivers[i]["driver_id"])]["call_driver"]["booking"][
                "booking_details"].format(
                name=get_user_base_info_action(cursor, user_id=user_id)["name"],
                rating=get_user_base_info_action(cursor, user_id=user_id)["rating"],
                location=get_info_by_coordinates(location.latitude, location.longitude),
                destination=get_info_by_coordinates(destination.latitude, destination.longitude),
                passengers_count=passengers_count,
                baggage=translations[get_language(user_id=message.from_user.id)]["yes"] if baggage else
                translations[get_language(user_id=message.from_user.id)]["no"],
                child_seat=translations[get_language(user_id=message.from_user.id)]["yes"] if child_seat else
                translations[get_language(user_id=message.from_user.id)]["no"],
                date=date,
                time=time,
            ),
            reply_markup=keyboards.core.accept_booking_driver_keyboard(drivers[i]["driver_id"], hash_id),
        )


def submit_booking(bot, message, cursor, user_id, hash_id):
    booking = None

    for key, unapproved_booking in unapproved_bookings.items():
        if key == hash_id:
            booking = unapproved_booking
            break

    if booking is None:
        print("Booking not found")
        return

    # msg for driver
    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]
        ["call_driver"]["booking"]["booking_accepted_driver"].format(
            name=get_user_base_info_action(cursor, booking["passenger_id"])["name"],
            telegram_username=booking["passenger_username"],
        ),
        reply_markup=types.ReplyKeyboardRemove(),
    )

    # msg for passenger
    bot.send_message(
        chat_id=booking["passenger_id"],
        text=translations[get_language(user_id=booking["passenger_id"])]["call_driver"]["booking"]
        ["booking_accepted_passenger"],
        reply_markup=types.ReplyKeyboardRemove(),
    )


def choose_driver(bot, message, cursor, user_id, driver_id):
    try:
        call = unapproved_calls[user_id]
    except KeyError:
        print("Call not found")
        return

    try:
        if call["driver_id"] is not None:
            print("Driver already chosen")
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
            rating=user["rating"],
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
        return

    try:
        if call["confirmed_at"] is not None:
            print("Call already confirmed")
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
            telegram_username=call["passenger_username"],
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
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["leave_rating"]["message"],
    )
    bot.register_next_step_handler_by_chat_id(message.chat.id, leave_rating_stage_driver, bot, cursor, user_id,
                                              trip["id"])

    bot.send_message(
        chat_id=trip["passenger_id"],
        text=translations[get_language(user_id=trip["passenger_id"])]["call_driver"]["trip_ended"],
    )
    bot.send_message(
        chat_id=trip["passenger_id"],
        text=translations[get_language(user_id=trip["passenger_id"])]["leave_rating"]["message"],
    )
    # Create a new message object or similar for the passenger to use in the next step handler
    bot.register_next_step_handler_by_chat_id(trip["passenger_id"], leave_rating_stage_passenger, bot, cursor,
                                              trip["passenger_id"], trip["id"])


def leave_rating_stage_driver(message, bot, cursor, user_id, trip_id):
    if message.text not in ["1", "2", "3", "4", "5"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["enter_number"],
        )
        bot.register_next_step_handler(message, leave_rating_stage_driver, bot, cursor, user_id, trip_id)
        return

    new_rating = int(message.text)

    cursor.execute("SELECT driver_id, passenger_id FROM trips WHERE id = %s", (trip_id,))
    trip = cursor.fetchone()

    if trip is None:
        print("Trip not found")
        return

    passenger_id = trip[1]

    raw_data = get_passenger_rating_info_action(cursor, passenger_id)

    rating = raw_data["rating"]
    rating_count = raw_data["rating_count"]

    if rating is not None and rating_count is not None:
        new_rating = (rating * rating_count + new_rating) / (rating_count + 1)
        rating_count += 1

    elif rating is None and rating_count is None:
        new_rating = new_rating
        rating_count = 1

    else:
        print("Error in rating calculation")
        return

    update_action(cursor, "passengers", "rating", new_rating, passenger_id)
    update_action(cursor, "passengers", "rating_count", rating_count, passenger_id)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["leave_rating"]["success"],
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
        reply_markup=keyboards.core.main_menu_keyboard(user_id, "driver"),
    )


def leave_rating_stage_passenger(message, bot, cursor, user_id, trip_id):
    if message.text not in ["1", "2", "3", "4", "5"]:
        bot.send_message(
            chat_id=message.chat.id,
            text=translations[get_language(user_id=user_id)]["errors"]["enter_number"],
        )
        bot.register_next_step_handler(message, leave_rating_stage_passenger, bot, cursor, user_id, trip_id)
        return

    new_rating = int(message.text)

    cursor.execute("SELECT driver_id, passenger_id FROM trips WHERE id = %s", (trip_id,))
    trip = cursor.fetchone()

    if trip is None:
        print("Trip not found")
        return

    driver_id = trip[0]

    raw_data = get_driver_rating_info_action(cursor, driver_id)

    rating = raw_data["rating"]
    rating_count = raw_data["rating_count"]

    if rating is not None and rating_count is not None:
        new_rating = (rating * rating_count + new_rating) / (rating_count + 1)
        rating_count += 1

    elif rating is None and rating_count is None:
        new_rating = new_rating
        rating_count = 1

    else:
        print("Error in rating calculation")
        return

    update_action(cursor, "drivers", "rating", new_rating, driver_id)
    update_action(cursor, "drivers", "rating_count", rating_count, driver_id)

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["leave_rating"]["success"],
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=translations[get_language(user_id=user_id)]["menus"]["main_menu"]["message"],
        reply_markup=keyboards.core.main_menu_keyboard(user_id, "passenger"),
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
