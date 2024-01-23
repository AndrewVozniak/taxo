from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from temporary_storages.main import unapproved_calls
from translations.core import translations, get_language
from database.actions.get_user_base_info import get_user_base_info_action
from keyboards.core import cancel_trip_keyboard
from database.actions.get_trip_details_by_passenger_id import get_trip_details_by_passenger_id_action


def cancel_call_if_not_confirmed(bot, cursor, user_id):
    call = unapproved_calls.get(user_id)

    if call and not call.get("confirmed_at"):
        passenger_name = get_user_base_info_action(cursor, user_id)["name"]

        bot.send_message(
            chat_id=user_id,
            text=translations[get_language(user_id=user_id)]["call_driver"]["time_over_cancel"],
        )

        bot.send_message(
            chat_id=call["driver_id"],
            text=translations[get_language(user_id=call["driver_id"])]["call_driver"]["time_over_cancel_driver"].format(
                name=passenger_name,
            ),
        )

        del unapproved_calls[user_id]


def show_cancel_button_if_arrival_time_too_long(bot, cursor, user_id):
    call = get_trip_details_by_passenger_id_action(cursor, user_id)

    if call and call.get("status") == "waiting":
        bot.send_message(
            chat_id=user_id,
            text=translations[get_language(user_id=user_id)]["call_driver"]["you_can_cancel"],
            reply_markup=cancel_trip_keyboard(user_id))


def send_advertisements(bot, cursor):
    print("Sending advertisements...")

    current_time = datetime.now()
    cursor.execute("SELECT * FROM advertisements WHERE %s BETWEEN start_date AND end_date", (current_time,))
    ads = cursor.fetchall()

    for ad in ads:
        cursor.execute("SELECT id FROM drivers UNION SELECT id FROM passengers")
        users = cursor.fetchall()

        # Если есть картинка
        if ad[1]:
            for user in users:
                user_id = user[0]
                try:
                    with open(ad[1], 'rb') as photo:
                        bot.send_photo(chat_id=user_id, photo=photo, caption=ad[4])

                except Exception as e:
                    print(e)
                    pass

        # Если нет картинки
        else:
            for user in users:
                user_id = user[0]

                try:
                    bot.send_message(chat_id=user_id, text=ad[2])
                except Exception as e:
                    print(e)
                    pass


scheduler = BackgroundScheduler()
scheduler.start()
