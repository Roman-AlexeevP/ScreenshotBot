import urllib

from aiogram import types
from aiogram.utils.callback_data import CallbackData

callback_factory = CallbackData("whois", "action", "url")


def whois_keybord_factory(url: str) -> types.InlineKeyboardMarkup:
    domain = urllib.parse.urlparse(url).netloc
    whois_button = types.InlineKeyboardButton(
        text="Подробнее(WHOIS)",
        callback_data=callback_factory.new(action="get_whois", url=domain)
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(whois_button)
    return keyboard
