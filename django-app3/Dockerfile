FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Установка зависимостей
COPY ./kursyamls/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем проект
COPY ./kursyamls /app

# Создание директорий для статики
RUN mkdir -p /app/static && mkdir -p /app/media

# Сборка статики на первом запуске
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn kursyamls.wsgi:application --bind 0.0.0.0:8000"]
