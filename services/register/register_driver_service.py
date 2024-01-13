from translations.core import translations, get_language
from keyboards.core import yes_no_keyboard


def init(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_name"])
    bot.register_next_step_handler(message, enter_name_stage, bot, cursor, user_id)


def enter_name_stage(message, bot, cursor, user_id):
    name = message.text
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_car_brand"])
    bot.register_next_step_handler(message, enter_car_brand_stage, bot, cursor, user_id, name)


def enter_car_brand_stage(message, bot, cursor, user_id, name):
    car_brand = message.text
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_seating_capacity"])
    bot.register_next_step_handler(message, enter_seating_capacity_stage,
                                   bot, cursor, user_id, name, car_brand)


def enter_seating_capacity_stage(message, bot, cursor, user_id, name, car_brand):
    seating_capacity = message.text
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["register"]["enter_is_child_seat"],
                     reply_markup=yes_no_keyboard(user_id))
    bot.register_next_step_handler(message, enter_is_child_seat_stage,
                                   bot, cursor, user_id, name, car_brand, seating_capacity)


def enter_is_child_seat_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity):
    is_child_seat = message.text

    if is_child_seat != translations[get_language(user_id=user_id)]["yes"] and is_child_seat != \
            translations[get_language(user_id=user_id)]["no"]:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["errors"]["choose_from_list"])
        bot.register_next_step_handler(message, enter_is_child_seat_stage,
                                       bot, cursor, user_id, name, car_brand, seating_capacity)

    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_about"])
    bot.register_next_step_handler(message, enter_about_stage,
                                   bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat)


def enter_about_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat):
    about = message.text

    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["is_it_correct"])
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["register"]["driver_info"].format(
                         name=name,
                         car_brand=car_brand,
                         seating_capacity=seating_capacity,
                         is_child_seat=is_child_seat,
                         about=about),
                     reply_markup=yes_no_keyboard(user_id))

    bot.register_next_step_handler(message, confirm_stage,
                                   bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat, about)


def confirm_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat, about):
    is_correct = message.text

    if is_child_seat == translations[get_language(user_id=user_id)]["yes"]:
        is_child_seat = True
    else:
        is_child_seat = False

    if is_correct == translations[get_language(user_id=user_id)]["yes"]:
        cursor.execute(
            """INSERT INTO drivers (id, name, car_brand, seating_capacity, has_child_seat, about) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, name, car_brand, seating_capacity, is_child_seat, about))
    else:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_name"])
        bot.register_next_step_handler(message, enter_name_stage,
                                       bot, cursor, user_id)
        return

    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["success_register"])
