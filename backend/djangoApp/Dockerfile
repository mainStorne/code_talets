# 1. официальный образ Python
FROM python:3.12-slim

# 2. устанавливаем переменные окружения для работы с приложением
ENV PYTHONDONTWRITEBYTECODE 1  # Отключаем создание .pyc файлов
ENV PYTHONUNBUFFERED 1  # Убеждаемся, что вывод логов сразу идет в консоль (без буферизации)

# 3. устанавливаем рабочую директорию в контейнере
WORKDIR /app

# 4. копируем файлы проекта в контейнер
COPY . /app/

# 5. устанавливаем зависимости проекта из файла requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. открываем порт 8000 для доступа к приложению
EXPOSE 8000

# 7. команда для запуска приложения
CMD ["gunicorn", "djangoApp.wsgi", "-b", "0.0.0.0:8000"]
