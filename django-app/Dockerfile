FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ������������� ����������� �����������
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./kursyamls/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./kursyamls /app

# ��������, ��� ������ ���������� ����
RUN mkdir -p /app/static && mkdir -p /app/media

# collectstatic � ������ gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn kursyamls.wsgi:application --bind 0.0.0.0:8000"]
