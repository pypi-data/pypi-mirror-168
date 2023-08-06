from django.conf import settings

from src.badi_utils.errors import BadiErrorCodes

default_lang = getattr(settings, "BADI_I18N", "fa")
i18n_values = {
    'fa': {
        BadiErrorCodes.permission_denied: 'شما دسترسی به این بخش ندارید!',
        "custom": "سفارشی",
        "login": "ورود",
        "logout": "خروج",

    },
    'en': {
        BadiErrorCodes.permission_denied: 'You dont have permission to this section!',

    },
}


class BadiI18n:
    lang = default_lang

    def __init__(self, lang=default_lang) -> None:
        self.lang = lang

    @classmethod
    def t(cls, value):
        return i18n_values[cls.lang].get(value, value)
