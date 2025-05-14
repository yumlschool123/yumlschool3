FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./kursyamls/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./kursyamls /app

# Убедимся, что нужные директории есть
RUN mkdir -p /app/static && mkdir -p /app/media

# collectstatic и запуск gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn kursyamls.wsgi:application --bind 0.0.0.0:8000"]
