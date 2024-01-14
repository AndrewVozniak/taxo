from helpers.get_info_by_coordinates import get_info_by_coordinates
from keyboards.core import yes_no_keyboard, main_menu_keyboard
from translations.core import translations, get_language
from database.actions.update_row import update_action
from database.actions.delete_row import delete_action


def edit_data(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_name"])
    bot.register_next_step_handler(message, enter_name_stage, bot, cursor, user_id)


def enter_name_stage(message, bot, cursor, user_id):
    name = message.text
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_car_brand"])
    bot.register_next_step_handler(message, enter_car_brand_stage, bot, cursor, user_id, name)


def enter_car_brand_stage(message, bot, cursor, user_id, name):
    car_brand = message.text
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_seating_capacity"])
    bot.register_next_step_handler(message, enter_seating_capacity_stage, bot, cursor, user_id, name, car_brand)


def enter_seating_capacity_stage(message, bot, cursor, user_id, name, car_brand):
    seating_capacity = message.text
    if not seating_capacity.isdigit():
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["errors"]["enter_number"])
        bot.register_next_step_handler(message, enter_seating_capacity_stage, bot, cursor, user_id, name, car_brand)
        return
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_is_child_seat"],
                     reply_markup=yes_no_keyboard(user_id))
    bot.register_next_step_handler(message, enter_is_child_seat_stage, bot, cursor, user_id, name, car_brand,
                                   seating_capacity)


def enter_is_child_seat_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity):
    is_child_seat = message.text
    if is_child_seat != translations[get_language(user_id=user_id)]["yes"] and is_child_seat != \
            translations[get_language(user_id=user_id)]["no"]:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["errors"]["choose_from_list"])
        bot.register_next_step_handler(message, enter_is_child_seat_stage, bot, cursor, user_id, name, car_brand,
                                       seating_capacity)
        return
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_about"])
    bot.register_next_step_handler(message, enter_about_stage, bot, cursor, user_id, name, car_brand, seating_capacity,
                                   is_child_seat)


def enter_about_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat):
    about = message.text
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["is_it_correct"])
    bot.send_message(message.chat.id,
                     translations[get_language(user_id=user_id)]["register"]["driver_info"]
                     .format(name=name,
                             car_brand=car_brand,
                             seating_capacity=seating_capacity,
                             is_child_seat=is_child_seat,
                             about=about),
                     reply_markup=yes_no_keyboard(user_id))
    bot.register_next_step_handler(message, is_it_correct_stage, bot, cursor, user_id, name, car_brand,
                                   seating_capacity, is_child_seat, about)


def is_it_correct_stage(message, bot, cursor, user_id, name, car_brand, seating_capacity, is_child_seat, about):
    is_correct = message.text
    if is_correct == translations[get_language(user_id=user_id)]["yes"]:
        driver_info = {
            "name": name,
            "car_brand": car_brand,
            "seating_capacity": seating_capacity,
            "has_child_seat": is_child_seat,
            "about": about,
        }

        for key, value in driver_info.items():
            update_action(cursor, 'drivers', key, value, user_id)

        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["edit_data"]["success"])
    elif is_correct == translations[get_language(user_id=user_id)]["no"]:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["register"]["enter_name"])
        bot.register_next_step_handler(message, enter_name_stage, bot, cursor, user_id)
    else:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["errors"]["choose_from_list"])
        bot.register_next_step_handler(message, is_it_correct_stage, bot, cursor, user_id, name, car_brand,
                                       seating_capacity, is_child_seat, about)


def delete_profile(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["delete_profile"]["message"],
                     reply_markup=yes_no_keyboard(user_id))
    bot.register_next_step_handler(message, delete_profile_stage, bot, cursor, user_id)


def delete_profile_stage(message, bot, cursor, user_id):
    answer = message.text
    if answer == translations[get_language(user_id=user_id)]["yes"]:
        delete_action(cursor, 'drivers', user_id)
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["delete_profile"]["success"])
    else:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["delete_profile"]["cancel"])


def set_my_geo_position(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["set_my_geo_position"]["message"])
    bot.register_next_step_handler(message, set_my_geo_position_stage, bot, cursor, user_id)


def set_my_geo_position_stage(message, bot, cursor, user_id):
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude

        update_action(cursor, 'drivers', 'current_location', f"{latitude},{longitude}", user_id)

        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["set_my_geo_position"]["success"]
                         .format(geo_position=get_info_by_coordinates(latitude, longitude)))
        set_my_radius(bot, message, cursor, user_id)
    else:
        bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["set_my_geo_position"]["error"])


def set_my_radius(bot, message, cursor, user_id):
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["set_my_geo_position"]["radius"])
    bot.register_next_step_handler(message, set_my_radius_stage, bot, cursor, user_id)


def set_my_radius_stage(message, bot, cursor, user_id):
    if message.text.isdigit():
        update_action(cursor, 'drivers', 'active_radius', message.text, user_id)
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["set_my_geo_position"]["success_radius"]
                         .format(active_radius=message.text))
    else:
        bot.send_message(message.chat.id,
                         translations[get_language(user_id=user_id)]["set_my_geo_position"]["error_radius"])
        bot.register_next_step_handler(message, set_my_radius_stage, bot, cursor, user_id)


def go_online(bot, message, cursor, user_id):
    update_action(cursor, 'drivers', 'is_active', True, user_id)
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["duty"]["now_you_online"],
                     reply_markup=main_menu_keyboard(user_id, 'driver', True))


def go_offline(bot, message, cursor, user_id):
    update_action(cursor, 'drivers', 'is_active', False, user_id)
    bot.send_message(message.chat.id, translations[get_language(user_id=user_id)]["duty"]["now_you_offline"],
                     reply_markup=main_menu_keyboard(user_id, 'driver', False))
