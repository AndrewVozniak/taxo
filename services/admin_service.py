import config

from datetime import datetime
from helpers.is_admin import is_admin
from jobs.main import scheduler, send_advertisements
from keyboards.core import cancel_keyboard
from translations.core import translations, get_language
from telebot import types


def init(bot, cursor, user_id, entered_password):
    if entered_password == config.ADMIN_PASSWORD:
        cursor.execute("INSERT INTO admins (id) VALUES (%s)", (user_id,))
        cursor.connection.commit()
        bot.send_message(user_id, translations[get_language(user_id=user_id)]["admin"]["you_being_admin"])
        return

    if is_admin(cursor, user_id):
        keyboards = types.InlineKeyboardMarkup()
        keyboards.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["change_ad_interval"],
            callback_data="change_ad_interval"
        ))
        keyboards.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["change_charity_wallet"],
            callback_data="change_charity_wallet"
        ))
        keyboards.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["get_feedbacks"],
            callback_data="get_feedbacks"
        ))

        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["you_already_admin"],
                         reply_markup=keyboards)
        return

    return


def change_charity_wallet(bot, message, cursor, user_id):
    if not is_admin(cursor, user_id):
        return

    bot.send_message(user_id,
                     translations[get_language(user_id=user_id)]["admin"]["change_charity_wallet"]["send_wallet"],
                     reply_markup=cancel_keyboard(user_id))
    bot.register_next_step_handler(message, get_wallet_stage, bot, user_id)


def get_wallet_stage(message, bot, user_id):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["action_canceled"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    wallet = message.text
    config.CHARITY_WALLET = wallet

    bot.send_message(user_id,
                     translations[get_language(user_id=user_id)]["admin"]["change_charity_wallet"]["success"],
                     reply_markup=types.ReplyKeyboardRemove())


def change_ad_interval(bot, message, cursor, user_id):
    if not is_admin(cursor, user_id):
        return

    bot.send_message(user_id,
                     translations[get_language(user_id=user_id)]["admin"]["change_ad_interval"]["send_interval"],
                     reply_markup=cancel_keyboard(user_id))
    bot.register_next_step_handler(message, get_interval_stage, bot, cursor, user_id)


def get_interval_stage(message, bot, cursor, user_id):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["action_canceled"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    interval = message.text

    try:
        interval = float(interval)
    except Exception as e:
        print(e)
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["change_ad_interval"]["error"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_interval_stage, bot, cursor, user_id)

    config.AD_INTERVAL = interval

    scheduler.remove_job("send_advertisements")
    scheduler.add_job(send_advertisements, 'interval', id='send_advertisements', hours=interval,
                      args=[bot, cursor])

    bot.send_message(user_id,
                     translations[get_language(user_id=user_id)]["admin"]["change_ad_interval"]["success"],
                     reply_markup=types.ReplyKeyboardRemove())


def publish_ad(bot, cursor, message):
    if not is_admin(cursor, message.from_user.id):
        return

    bot.send_message(message.from_user.id,
                     translations[get_language(user_id=message.from_user.id)]["admin"]["publish_ad"][
                         "send_image_and_text"],
                     reply_markup=cancel_keyboard(message.from_user.id))
    bot.register_next_step_handler(message, get_image_and_text_stage, bot, cursor, message.from_user.id)


def get_image_and_text_stage(message, bot, cursor, user_id):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["action_canceled"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        if message.photo:
            image = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)

            with open(f"static/images/{message.photo[-1].file_id}.jpg", "wb") as f:
                f.write(image)
                image = f"static/images/{message.photo[-1].file_id}.jpg"

            text = message.caption
        else:
            image = None
            text = message.text

        print(image, text)

        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["send_start_date"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_start_date_stage, bot, cursor, user_id, image, text)

    except AttributeError:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["send_image_and_text"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_image_and_text_stage, bot, cursor, user_id,
                                       reply_markup=cancel_keyboard(user_id))
        return


def get_start_date_stage(message, bot, cursor, user_id, image, text):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["action_canceled"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        start_date = message.text
        start_date = datetime.strptime(start_date, "%d.%m.%Y %H:%M")

        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["send_end_date"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_end_date_stage, bot, cursor, user_id, image, text, start_date)

    except ValueError:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["use_format"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_start_date_stage, bot, cursor, user_id)
        return


def get_end_date_stage(message, bot, cursor, user_id, image, text, start_date):
    if message.text == translations[get_language(user_id=user_id)]["keyboards"]["cancel"]:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["action_canceled"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        end_date = message.text
        end_date = datetime.strptime(end_date, "%d.%m.%Y %H:%M")

        cursor.execute(
            "INSERT INTO advertisements (image, text, start_date, end_date) VALUES (%s, %s, %s, %s)",
            (image, text, start_date, end_date))
        cursor.connection.commit()

        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["ad_published"],
                         reply_markup=types.ReplyKeyboardRemove())

    except ValueError:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["publish_ad"]["use_format"],
                         reply_markup=cancel_keyboard(user_id))
        bot.register_next_step_handler(message, get_end_date_stage, bot, cursor, user_id, image, text, start_date)
        return


def get_feedbacks(bot, cursor, user_id):
    if not is_admin(cursor, user_id):
        return

    cursor.execute("SELECT * FROM feedbacks")
    data = cursor.fetchall()

    if not data:
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["admin"]["get_feedbacks"]["no_feedbacks"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    for feedback in data:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text=translations[get_language(user_id=user_id)]["keyboards"]["delete_feedback"],
            callback_data=f"delete_feedback_{feedback[0]}"
        ))

        feedback_message = translations[get_language(user_id=user_id)]["admin"]["get_feedbacks"]["feedback"]
        formatted_message = feedback_message.format(id=feedback[1], feedback=feedback[2])

        bot.send_message(user_id, formatted_message, reply_markup=keyboard)


def delete_feedback(bot, cursor, user_id, feedback_id):
    if not is_admin(cursor, user_id):
        return

    try:
        cursor.execute("DELETE FROM feedbacks WHERE id = %s", (feedback_id,))
        cursor.connection.commit()
    except Exception as e:
        print(e)
        bot.send_message(user_id,
                         translations[get_language(user_id=user_id)]["errors"]["unknown"],
                         reply_markup=types.ReplyKeyboardRemove())
        return

    bot.send_message(user_id,
                     translations[get_language(user_id=user_id)]["admin"]["delete_feedback"]["success"],
                     reply_markup=types.ReplyKeyboardRemove())
