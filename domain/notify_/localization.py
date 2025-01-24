from domain.notify_.locale.en import messages_en
from domain.notify_.locale.ru import messages_ru
from domain.notify_.locale.uk import messages_uk


def get_message(language, key, **kwargs):
    if language == 'en':
        messages = messages_en
    elif language == 'ru':
        messages = messages_ru
    elif language == 'uk':
        messages = messages_uk
    else:
        messages = messages_en

    message_template = messages.get(key, messages_en.get(key))

    return message_template.format(**kwargs)
