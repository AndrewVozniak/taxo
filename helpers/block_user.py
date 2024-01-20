from temporary_storages.main import failed_attempts_storage
from datetime import datetime, timedelta


def block_user(bot, message, user_id):
    if failed_attempts_storage.get(user_id) is None:
        failed_attempts_storage[user_id] = {'first_attempt': datetime.now(), 'block_duration': 5,
                                            'last_block_time': None}
    else:
        if failed_attempts_storage[user_id]['first_attempt'] is None:
            failed_attempts_storage[user_id]['first_attempt'] = datetime.now()

    current_time = datetime.now()
    attempt_info = failed_attempts_storage.get(user_id)

    time_since_first_attempt = current_time - attempt_info['first_attempt']
    time_since_last_block = current_time - attempt_info['last_block_time'] if attempt_info['last_block_time'] else None

    # Проверяем, не истек ли 10-минутный интервал с первой попытки
    if time_since_first_attempt >= timedelta(minutes=10):
        # Проверяем, истекла ли предыдущая блокировка
        if time_since_last_block is None or time_since_last_block > timedelta(minutes=attempt_info['block_duration']):
            # Пользователь не был заблокирован ранее или блокировка истекла
            if time_since_last_block is None:
                # Если это первая попытка, блокируем на 5 минут
                new_block_duration = 5
                # 0:00:00
                attempt_info['first_attempt'] = None
            elif attempt_info['block_duration'] == 5:
                # Вторая попытка, блокируем на 10 минут
                new_block_duration = 10
                attempt_info['first_attempt'] = None
            elif attempt_info['block_duration'] == 10:
                # Третья попытка, блокируем на 30 минут
                new_block_duration = 30
                attempt_info['first_attempt'] = None
            else:
                # Последующие попытки, оставляем блокировку на 30 минут
                new_block_duration = 30
                attempt_info['first_attempt'] = None

            attempt_info['block_duration'] = new_block_duration
            attempt_info['last_block_time'] = current_time
            failed_attempts_storage[user_id] = attempt_info
            # Отправляем сообщение о блокировке
            bot.send_message(chat_id=message.chat.id,
                             text="Вы заблокированы на {} минут из-за частых попыток вызова.".format(
                                 attempt_info['block_duration']))
        else:
            # Пользователь уже заблокирован
            bot.send_message(chat_id=message.chat.id, text="Вы уже заблокированы.")
            return
