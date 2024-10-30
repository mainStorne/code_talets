# link to google sheet: https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0

# Установка gspread
# pip install gspread
import gspread


# Подключение к Google Sheets через API
gc = gspread.service_account(filename='API_google_sheet.json')

# Открытие таблицы
wks = gc.open("kode_telegtam_bot").sheet1


def connect_to_db():
	print("Подключение к базе данных успешно установлено.")
	return True

# Утированное получение данных пользователя
def getDataOfUser():
	fio = 'Иван Иванов'
	email = 'ivan.ivanov@example.com'
	phoneNumber = '+1234567890'
	age = '30'
	city = 'Москва'
	created_at = '2024-10-30'
	telegram = '@ivan_ivanov'

	print("Данные пользователя успешно получены.")
	return fio, email, phoneNumber, age, city, created_at, telegram

# Функция для записи данных в Google Sheets
def writeDataToGoogleSheet():
	if connect_to_db():
		# Получаем данные пользователя
		fio, email, phoneNumber, age, city, created_at, telegram = getDataOfUser()

		# Подготавливаем данные для записи в Google Sheets
		new_data = [[fio, email, phoneNumber, age, city, created_at, telegram]]

		# Получаем последнюю строку для добавления данных в конец таблицы
		data = wks.get_all_values()
		last_row = len(data)

		# Запись данных в таблицу
		range_name = 'A' + str(last_row + 1) + ':G' + str(last_row + 1)
		wks.update(range_name, new_data)
		print("Данные успешно записаны в Google Sheets.")

# Вызов функции для записи данных
writeDataToGoogleSheet()
