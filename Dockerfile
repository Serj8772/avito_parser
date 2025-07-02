FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip fonts-liberation libxss1 libappindicator1 libnss3 \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 xdg-utils \
    chromium-driver chromium \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Образ основан на Debian, pip уже установлен
RUN pip install --no-cache-dir -r requirements.txt

# Переменные окружения
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

CMD ["python", "main.py"]