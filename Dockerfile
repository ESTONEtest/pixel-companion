FROM python:3.13-slim

# Устанавливаем FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом весь проект
COPY . .

# Запуск бота
CMD ["python", "main.py"]