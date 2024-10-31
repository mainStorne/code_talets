import httpx
from bs4 import BeautifulSoup


# def get_vacancies() -> list[str]:
url = 'https://career.kode.ru/career/'
response = httpx.get(url, verify=False)

if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
		headings = soup.find_all('a')
		for heading in headings:
			print(heading.text)
else:
		print('Ошибка при запросе:', response.status_code)

# get_vacancies()
print('a')
