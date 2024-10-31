import requests
from bs4 import BeautifulSoup

url = 'https://career.kode.ru/career/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Пример: извлечение всех заголовков h1
    headings = soup.find_all('h1')
    for heading in headings:
        print(heading.text)
else:
    print('Ошибка при запросе:', response.status_code)
