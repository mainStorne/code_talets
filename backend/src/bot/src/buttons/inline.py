from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo



def main_menu(domain: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Я знаю, какая специальность мне интересна', web_app=WebAppInfo(url=f'{domain}/send_request'))
    builder.button(text='Я не знаю, какая специальность мне интересна', web_app=WebAppInfo(url=f'{domain}/send_request?next=next'))
    builder.adjust(1)
    return builder.as_markup()