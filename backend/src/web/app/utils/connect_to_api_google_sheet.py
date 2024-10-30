# link to google sheet: https://docs.google.com/spreadsheets/d/1hH-zaxjEvBLexxqnOSbp8FyF7RfVeLnKhBq9izkNraY/edit?gid=0#gid=0

# pip install gspread
import gspread

gc = gspread.service_account(filename='API_google_sheet.json')

# Open a sheet from a spreadsheet in one go
wks = gc.open("kode_telegtam_bot").sheet1

#get all data
data = wks.get_all_values()
last_row = len(data)

fio = 'FIO'
email = 'email'
phoneNumber = 'phone_number'
age = 'age'
city = 'city'
application_submission_time = 'application_submission_time'
telegram = 'telegram'

new_data = [[f"{fio}", f"{email}", f"{phoneNumber}", f"{age}", f"{city}", f"{application_submission_time}", f"{telegram}"]]


wks.update(new_data, range_name='A' + str(last_row + 1) + ':H' + str(last_row + len(new_data)))
