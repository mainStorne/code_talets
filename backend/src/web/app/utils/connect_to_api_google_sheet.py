# link to google sheet: https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0
import logging

# pip install gspread
import gspread
from gspread import spreadsheet, Worksheet
from pathlib import Path

path = Path(__file__).absolute().parent


def init_google_sheet():
    logging.info(path)
    gc = gspread.service_account(filename=path / 'API_google_sheet.json')
    wks = gc.open("kode_telegtam_bot").sheet1
    return wks


def connect_to_db():
    print("Подключение к базе данных успешно установлено.")
    return True


def getDataOfUser() -> list[str]:
    fio = 'Иван Иванов'
    phoneNumber = '+1234567890'
    age = '30'
    city = 'Москва'
    created_at = '2024-10-30'
    telegram = '@ivan_ivanov'

    print("Данные пользователя успешно получены.")
    return [fio, phoneNumber, age, city, created_at, telegram]


def writeDataToGoogleSheet(wks: Worksheet, data: list[str]) -> None:
    if connect_to_db():
        new_data = [data]  # [[fio, email, phoneNumber, age, ...]]

        data = wks.get_all_values()
        last_row = len(data)

        range_name = 'A' + str(last_row + 1) + ':F' + str(last_row + 1)
        wks.update(range_name, new_data)
        logging.info("Данные успешно записаны в Google Sheets.")
