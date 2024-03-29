from translations import ru, en
from config import DEFAULT_LANGUAGE

translations = {
    'ru': ru.dataset,
    'en': en.dataset
}

default_language = DEFAULT_LANGUAGE

users_temporary_language = {}


def set_temporary_language(user_id, language):
    users_temporary_language[user_id] = language


def get_temporary_language(user_id):
    return users_temporary_language.get(user_id, default_language)


def delete_temporary_language(user_id):
    if user_id in users_temporary_language:
        del users_temporary_language[user_id]


def get_language(user_id):
    user_language = get_temporary_language(user_id)

    if user_language is None:
        set_temporary_language(user_id, default_language)
        user_language = default_language

    return user_language
