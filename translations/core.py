from translations import ru, en

translations = {
    'ru': ru.dataset,
    'en': en.dataset
}

default_language = 'en'

users_temporary_language = {}


def set_temporary_language(user_id, language):
    users_temporary_language[user_id] = language


def get_temporary_language(user_id):
    return users_temporary_language.get(user_id, default_language)


def get_language(user_id):
    user_language = get_temporary_language(user_id)

    if user_language is None:
        set_temporary_language(user_id, default_language)
        user_language = default_language

    return user_language
