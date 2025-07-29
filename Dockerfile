# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы в контейнер
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Указываем команду для запуска нашего сервера
CMD ["python", "rendezvous_server.py"]