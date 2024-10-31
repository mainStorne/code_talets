from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo


def main_menu(domain: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Я знаю, какая специальность мне интересна', web_app=WebAppInfo(url=f'{domain}/signup'))
    builder.button(text='Я не знаю, какая специальность мне интересна', web_app=WebAppInfo(url='https://9w8x7mzf-5173.use.devtunnels.ms/send_request'))
    builder.adjust(3)
    return builder.as_markup()