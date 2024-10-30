from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo


def main_menu(domain: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Не', web_app=WebAppInfo(url=f'{domain}/signup'))
    builder.button(text='Да', web_app=WebAppInfo(url=f'{domain}/route'))
    builder.adjust(3)
    return builder.as_markup()